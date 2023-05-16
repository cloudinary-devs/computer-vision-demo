# read from .env file
from dotenv import load_dotenv
load_dotenv()

# import Cloudinary libraries
import cloudinary
from cloudinary import uploader
import cloudinary.api
from cloudinary.utils import cloudinary_url

# import other libraries
import os
import threading
from collections import Counter
from urllib.request import urlopen
import ssl
import json

# get reference to config instance
# config = cloudinary.Config()
# print(config.cloud_name)
# print(config.api_key)

from flask import Flask, render_template, request
import json

app = Flask(__name__, static_url_path='/static')



@app.route("/", methods=['GET'])
def index():
  '''
  # Create the upload preset only once:
  cloudinary.api.create_upload_preset(
    name = "docs_computer_vision_demo",
    unsigned = True,  
    use_filename=True,
    folder="docs/computer_vision_demo",
    tags="computer_vision_demo",
    colors= True,
    faces= True,
    categorization = "google_tagging", auto_tagging = 0.7,
    ocr = "adv_ocr",
    moderation = "aws_rek"
  )
  '''
  
  #cloudinary.api.delete_resources_by_tag("computer_vision_demo") 
  
  return render_template('index.html', failed_upload='')


@app.route("/output", methods=['POST'])
def output():
  assetList=cloudinary.api.resources_by_tag("computer_vision_demo")
  print(len(assetList['resources']))
  if len(assetList['resources']) != 1 and len(assetList['resources']) != 2 and len(assetList['resources'])!=3:
    return render_template('index.html', failed_upload='Your upload failed. Try again!')
  publicIds=[]

  for asset in assetList['resources']:
    publicIds.append(asset["public_id"])

  urls=[]
  transformations=[]
  messages=[]
  num=len(publicIds)
  titles=[]

  for publicId in publicIds:
    message=""
    display="yes"
    details=cloudinary.api.resource(publicId, 
                                    faces=True, 
                                    colors=True)
    #print(json.dumps(details, indent=2))

    if details["moderation"][0]["status"]=="approved":
      url=details["secure_url"]
      transformation=url
      urls.append(url)
      # Tags
      #details["tags"].remove("computer_vision_demo")
      #message="This image shows a " + details["tags"][0]
      
      title=details["info"]["categorization"]["google_tagging"]["data"][0]["tag"] + " / " + details["info"]["categorization"]["google_tagging"]["data"][2]["tag"]+ " / " + details["info"]["categorization"]["google_tagging"]["data"][3]["tag"]
      titles.append(title)
      
      # OCR
      if "textAnnotations" in details["info"]["ocr"]["adv_ocr"]["data"][0]:
        word = details["info"]["ocr"]["adv_ocr"]["data"][0]
        message=message+"This picture contains the phrase '" + word["textAnnotations"][0]["description"] + "'.\n"
      else:
        message=message+"There aren't any words in this picture.\n\n"

      # Face detection
      faces=len(details["faces"])
      #print(details["faces"])
      if faces==0:
        message=message+"There aren't any faces in this picture.\n\n"
      elif faces==1:
        coordinates = details["faces"][0]
        message=message+"There is one face in this picture with coordinates: " + ' ,'.join(str(e) for e in coordinates)+ "\n"
      else:
        message=message+"There are " + str(faces) + " faces in this picture with coordinates:\n "
        for coordinates in (details["faces"]):
          message=message+' '.join(str(e) for e in coordinates)+' \n'
        message=message+"\n"

      # Orientation
      if details["width"]/details["height"]>1:
        orientation="landscape"
        message=message+"The orientation is Landscape.\n\n"
      elif details["width"]/details["height"]==1:
        orientation="square"
        message=message+"The picture is a square.\n\n"
      else:
        orientation="portrait"
        message=message+" The orientation is Portrait.\n\n"

      # Colors
      color1=details["colors"][0][0]
      color2=details["colors"][1][0]
      message=message+"The predominant colors are " + details["colors"][0][0] + " and " +  details["colors"][1][0] + "."
      
      # Build transformations
      place=url.find("upload/")+7


      # Add phone underlay
      if orientation=="portrait" or orientation=="square":
        transformation = url[ :place] +"u_iphone,w_1.7,h_1.7,fl_relative/"+ transformation[place: ]
      
      else:
        transformation = url[ :place] +"u_iphone,a_180,w_1.7,h_1.7,fl_relative/"+ transformation[place: ]
      

      # Place sunglasses over faces in images
      if faces>0:
        transformation=transformation[ :place] +"l_sunglasses_emoji/fl_layer_apply,w_1.1,fl_region_relative,g_faces/" + transformation[place: ]
        
      
      # Make border using pedominant colors
      if faces==0:
        color1=color1.replace("#","")
        color2=color2.replace("#","")
        transformation = transformation[ :place] + "b_rgb:"+color1+"/bo_35px_solid_rgb:"+color2+"/"+ transformation[place: ]

      transformation=transformation[ :place] +"h_300/f_auto/q_auto/" + transformation[place: ]
      #print(transformation)
      transformations.append(transformation)
      messages.append(message)
    else:
      display="no"
      message="This picture doesn't meet Cloudinary's standards."
    #print(message)

  return render_template('output.html', titles=titles, num=num, urls=urls, transformations=transformations, messages=messages, color1=color1, color2=color2)

if __name__ == "__main__":
  app.run()