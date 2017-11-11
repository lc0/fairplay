"""Simple API to serve encrypted files to Providers."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from flask import Flask, jsonify, send_from_directory, request

import os

from utils import extract_by_key

app = Flask(__name__)
working_dir = os.getcwd()
FILES_PREFIX = 'user_files'


@app.route("/")
def index():
    """Home page."""
    return jsonify({'message': 'hello'})


@app.route('/file/<string:uid>/<string:public_key>', methods=['GET'])
def serve_files(uid, public_key):
    """Serve static files."""
    file_path = os.path.join(working_dir, FILES_PREFIX, uid)
    app.logger.info('Processing file {}'.format(file_path))

    return send_from_directory(file_path, public_key)


# TODO: ensure it's a real app
# TODO: check a signature
@app.route('/file/<string:uid>/<string:public_key>', methods=['POST'])
def store_data(uid, public_key):
    """Store user encrypted data."""
    if 'file' not in request.files:
        response = jsonify({'error': 'not provided, some issues with content-type?'})
        response.status_code = 400
        return response

    file = request.files['file']

    file_folder = os.path.join(working_dir, FILES_PREFIX, uid)
    if not os.path.isdir(file_folder):
        os.makedirs(file_folder)

    file_path = os.path.join(file_folder, public_key)
    app.logger.info('Received a file from {}; storing to {}'.format(uid, file_path))
    file.save(file_path)

    return jsonify({'message': 'Successfully stored'})


# TODO: add a proper queue
@app.route('/process-block', methods=['POST'])
def process_block():
    """Process a new update from blockchain."""
    block_meta = request.get_json()
    app.logger.info("Received process-block request {}".format(block_meta))

    # TODO: move this processing to a separate thread
    user_id = block_meta['user_id']
    key_scopes = extract_by_key(block_meta['scopes'])

    app.logger.info("Triggering event to user {} with request {}".format(user_id, key_scopes))

    return jsonify({'message': 'Queued to process encode a file'})


# Run the server app
if __name__ == "__main__":
    app.debug = True
    app.config['UPLOAD_FOLDER'] = FILES_PREFIX
    app.run()
    app.run(debug=True)
