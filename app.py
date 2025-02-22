from flask import Flask, render_template, request
from PIL import Image
from base64 import b64encode
from io import BytesIO
import time
import requests

app = Flask(__name__)

# Hugging Face API details
API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
HEADERS = {"Authorization": "Bearer token"}

# Call the local image generation API
def generate_similar_image(caption):
    try:
        response = requests.get(
            "http://127.0.0.1:5000/generate-image", 
            params={"prompt": caption}
        )
        response.raise_for_status()
        return response.json().get('image', '')
    except Exception as e:
        raise ValueError(f"Error generating similar image: {e}")

def convert_image_to_base64(image):
    with Image.open(image).convert('RGB') as pil_image:
        buffered = BytesIO()
        pil_image.save(buffered, format="JPEG")
        return b64encode(buffered.getvalue()).decode('utf-8')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image = request.files.get('image')
        if not image:
            return render_template('index.html', generation_message="No image provided")

        # Start the overall timer
        overall_start_time = time.time()

        try:
            # Generate caption
            caption_start_time = time.time()
            response = requests.post(API_URL, headers=HEADERS, data=image)
            response.raise_for_status()
            caption = response.json()[0]['generated_text']
            caption_generation_time = time.time() - caption_start_time
        except Exception as e:
            return render_template('index.html', generation_message=f"Error: {str(e)}")

        try:
            # Generate similar image
            similar_image_base64 = generate_similar_image(caption)
        except ValueError as e:
            similar_image_base64 = ""
            generation_message = f"Caption generated in {caption_generation_time:.2f} seconds | {str(e)}"
            return render_template(
                'index.html',
                image=convert_image_to_base64(image),
                caption=caption,
                similar_image=similar_image_base64,
                generation_message=generation_message
            )

        # Calculate overall time
        overall_end_time = time.time()
        overall_generation_time = overall_end_time - overall_start_time

        generation_message = f"Caption and similar image generated in {overall_generation_time:.2f} seconds"

        return render_template(
            'index.html',
            image=convert_image_to_base64(image),
            caption=caption,
            similar_image=similar_image_base64,
            generation_message=generation_message
        )

    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
