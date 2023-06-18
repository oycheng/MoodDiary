from flask import Flask, request, jsonify, render_template, send_from_directory
import tensorflow as tf
import numpy as np
from flask_cors import CORS

from routes_chat import bp as chat_bp

app = Flask(__name__)
CORS(app)

# Register the routes Blueprints
app.register_blueprint(chat_bp)


@app.route('/')
def handle_request():
    return 'Connected to Server'


# Run the application
if __name__ == '__main__':
    # change host to local IP address for hardware public request
    # app.run(host="172.20.10.3")
    app.run(host='0.0.0.0', port=5000)