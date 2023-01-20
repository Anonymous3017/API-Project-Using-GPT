from flask import Flask, jsonify, request, Response, render_template
from qrcode import QRCode
from PIL import Image
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/qrcode', methods=['GET', 'POST'])
def generate_qrcode():
    # Get the URL from the GET request's query parameters
    url = request.form.get('url')
    # If the URL is not provided, return an error
    if not url:
        return jsonify({'error': 'URL parameter is required'}), 400
    try:
        # Generate QR code image

        qr = QRCode(version=1, box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="transparent")

        #img = qrcode.make(url)

        # Open custom image
        if 'custom_img' in request.files:
            custom_img = Image.open(request.files['custom_img'].stream).convert("RGBA")
        else:
            return jsonify({'error': 'custom_img is missing in the request'}), 400


        # Resize custom image to the same size of QR code
        custom_img = custom_img.resize((img.size[0], img.size[1]))

        # Create a transparent QR code by adding alpha channel
        img = img.convert("RGBA")

        #edit
        # Open white image with transparency
        white_img = Image.new('RGBA', img.size, (255, 255, 255, 80))

        # Paste the white image on top of the custom image
        custom_img.paste(white_img, (0, 0), white_img)

        # Overlay the QR code on top of the custom image
        img = Image.alpha_composite(custom_img, img)

        # Save the QR code image to a buffer
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        # Create a response object with the image buffer
        response = Response(buffer.read(), content_type='image/png')
        response.headers["Content-Disposition"] = "attachment; filename=qrcode.png"
        return response
    except Exception as e:
        # Return an error if there was an exception
        return jsonify({'error': str(e)}), 500

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
