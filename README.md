# computer-vision-demo
Here's a small taste of what you create with Cloudinary's vast analysis capabilities. The possibilities are endless! 

In this demo, you'll be asked upload up to 3 images. Cloudinary will analyze those assets and return the images automatically transformed accordingly along with a description. 


## Setup instructions (after cloning from GitHub)

1. **Enable required add-ons**
   Go to the [Add-ons](https://console.cloudinary.com/settings/addons) page of the Console Settings and enable:
   * **Google Auto Tagging**
   * **OCR Text Detection and Extraction**
   * **Amazon Rekognition AI Moderation**

2. **Create a virtual environment**
   
    ```
    python3 -m venv venv
    ```

3. **Activate your virtual environment**
   
    ```
    source venv/bin/activate
    ```

4. **Install dependencies**
   
    ```
    pip install -r requirements.txt
    ```

5. **Create a `.env` file**
   Add the following environment variable:
  
    ```
    CLOUDINARY_URL=cloudinary://<api_key>:<api_secret>@<cloud_name>
    ``` 
   
6. **Replace placeholders**
   Update the `.env` file with your Cloudinary credentials, which you can find in the [API Keys](https://console.cloudinary.com/settings/api-keys) page of the Console Settings.

7. **Update the `cloudName` value**
   In `index.html`, replace the value for `cloudName` with your Cloudinary cloud name.

8. **(First-time only) Create the upload preset**
   In `demo.py`, uncomment the following block inside the `index()` route the first time you run the app:

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

    {note}
    Remember to replace the comments after the first run.
    {/note}

   
9.  **Run the Flask app**
    
    ```
    python demo.py
    ```
