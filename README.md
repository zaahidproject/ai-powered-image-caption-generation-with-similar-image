# Image Captioning and Similar Image Generation

This project is a Flask-based web application that generates image captions using the **Salesforce BLIP Image Captioning Large** model from Hugging Face and then creates a similar image using the **Stable Diffusion XL Base 1.0** model. The application consists of two components:

1. **Main Flask App (app.py)** - Handles image uploads, sends them to Hugging Face for captioning, and retrieves a generated similar image.
2. **Image Generation API (api.py)** - A separate service running on port `5000` that generates similar images based on text prompts.

## Features
- Upload an image and generate a caption using Hugging Face's `Salesforce/blip-image-captioning-large` model.
- Use the generated caption as a prompt to create a similar image with Hugging Face's `stabilityai/stable-diffusion-xl-base-1.0` model.
- Display the original image, generated caption, and similar image in a web interface.

## File Structure
```
image-captioning-similar-image/
│── api.py                # Image generation API
│── app.py                # Main Flask application
│── README.md             # Project documentation
│── requirements.txt      # Dependencies list
│── templates/            # HTML templates for the web interface
│── venv/                 # Virtual environment (optional)
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/image-captioning-similar-image.git
   cd image-captioning-similar-image
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Set up your Hugging Face API token by replacing the placeholder in `app.py` and `api.py`:
   ```python
   HEADERS = {"Authorization": "Bearer YOUR_HUGGINGFACE_API_KEY"}
   ```

## Running the Application

1. Start the **Image Generation API** (Runs on port `5000`):
   ```bash
   python3 api.py
   ```
2. Start the **Main Flask Application** (Runs on port `8000`):
   ```bash
   python3 app.py
   ```
3. Open your browser and go to:
   ```
   http://localhost:8000
   ```

## Workflow
1. User uploads an image via the web interface.
2. The image is sent to the **Hugging Face BLIP Model** for caption generation.
3. The generated caption is then used as a prompt for the **Stable Diffusion Model** to create a similar image.
4. The original image, generated caption, and similar image are displayed on the web interface.

## API Endpoints

### Main Flask App (`app.py`)
- **`/`** (Home) - Upload an image and generate a caption & similar image.

### Image Generation API (`api.py`)
- **`/generate-image`** (GET) - Accepts a text prompt and returns a base64-encoded image.
  
  **Example Request:**
  ```bash
  curl -X GET "http://127.0.0.1:5000/generate-image?prompt=A beautiful sunset over the ocean"
  ```

## Dependencies
- Flask
- PIL (Pillow)
- Requests
- Hugging Face `huggingface_hub`

## Notes
- Ensure both Flask applications (`app.py` and `api.py`) are running for full functionality.
- You need a valid Hugging Face API token to use the models.
- The project is designed to be modular, allowing different image captioning and generation models to be used.

## License
This project is licensed under the MIT License.

