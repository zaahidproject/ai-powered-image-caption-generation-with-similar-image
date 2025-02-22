from flask import Flask, request, jsonify
from huggingface_hub import InferenceClient
import io
import base64
from PIL import Image

app = Flask(__name__)

# Initialize the client
client = InferenceClient("stabilityai/stable-diffusion-xl-base-1.0", 
                         token="token")

@app.route('/generate-image', methods=['GET'])
def generate_image():
    try:
        prompt = request.args.get('prompt', default=None, type=str)
        
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400
        image = client.text_to_image(prompt)
        
        if not isinstance(image, Image.Image):
            return jsonify({"error": "Invalid image format returned"}), 500

        img_io = io.BytesIO()
        image.save(img_io, 'PNG')
        img_io.seek(0)

        image_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

        return jsonify({"image": image_base64})

    except Exception as e:
        return jsonify({"error": "Internal server error. Please try again."}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
