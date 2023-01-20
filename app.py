from flask import Flask, jsonify, request
from flask_qrcode import QRcode
import qrcode
import io

# Create a new Flask application
app = Flask(__name__)

# Initialize QRcode extension
QRcode(app)

# Create endpoint '/qrcode' for GET request
@app.route('/qrcode', methods=['GET'])
def generate_qrcode():
    # Get the URL from the GET request's query parameters
    url = request.args.get('url')
    # If the URL is not provided, return an error
    if not url:
        return jsonify({'error': 'URL parameter is required'}), 400
    try:
        # Generate the QR code image
        img = qrcode.make(url)
        # Save the QR code image to a file
        img.save('qrcode.png')
        # Return the image file as the response
        return app.response_class(open('qrcode.png', 'rb'), content_type='image/png')
    except Exception as e:
        # Return an error if there was an exception
        return jsonify({'error': str(e)}), 500

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
