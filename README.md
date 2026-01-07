# computer-vision-demo
Here's a small taste of what you create with Cloudinary's vast analysis capabilities. The possibilities are endless! 

In this demo, you'll be asked upload up to 3 images. Cloudinary will analyze those assets and return the images automatically transformed accordingly along with a description. 


## Setup instructions (after cloning from GitHub)

1. **Navigate to the project directory**
   <p>After cloning the repository, navigate into it:</p>

   ```
   cd computer-vision-demo
   ```

3. **Enable required add-ons**
   <p>Go to the <a href="https://console.cloudinary.com/settings/addons">Add-ons</a> page of the Console Settings and enable:</p>
   * **Auto Tagging by Google**
   * **OCR Text Detection and Extraction**
   * **AI Moderation by Amazon Rekognition**

4. **Create a virtual environment**
   
    ```
    python3 -m venv venv
    ```

5. **Activate your virtual environment**
   
    ```
    source venv/bin/activate
    ```

6. **Install dependencies**
   
    ```
    pip install -r requirements.txt
    ```

7. **Create a `.env` file**
   <p>Add the following environment variable:</p>
  
    ```
    CLOUDINARY_URL=cloudinary://<api_key>:<api_secret>@<cloud_name>
    ``` 
   
8. **Replace placeholders**
   <p>Update the <code>.env</code> file with your Cloudinary credentials, which you can find in the <a href="https://console.cloudinary.com/settings/api-keys">API Keys</a> page of the Console Settings.</p>

9. **Update the `cloudName` value**
   <p>In <code>index.html</code>, replace the value for <code>cloudName</code> with your Cloudinary cloud name.</p>

10. **(First-time only) Create the upload preset**
   <p>In <code>demo.py</code>, uncomment the following block inside the <code>index()</code> route the first time you run the app:</p>

    ```
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
      ```

    **Note:** Remember to replace the comments after the first run.
   
11.  **Run the Flask app**
    
    ```
    python demo.py
    ```
