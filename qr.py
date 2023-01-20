from flask import Flask, jsonify, request, Response
import qrcode
from io import BytesIO

# Initialize Flask application
app = Flask(__name__)

# Create endpoint '/qrcode' for GET request
@app.route('/qrcode', methods=['GET'])
def generate_qrcode():
    # Get the URL from the GET request's query parameters
    url = request.args.get('url')
    # If the URL is not provided, return an error
    if not url:
        return jsonify({'error': 'URL parameter is required'}), 400
    try:
        # Generate QR code image
        img = qrcode.make(url)
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
