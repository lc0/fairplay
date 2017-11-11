"""Simple API to serve encrypted files to Providers."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from flask import Flask, jsonify, send_from_directory, request, url_for

import os

from utils import extract_by_key

app = Flask(__name__)
working_dir = os.getcwd()
FILES_PREFIX = 'user_files'


@app.route("/")
def index():
    """Home page."""
    return jsonify({'message': 'hello'})


@app.route('/file/<string:uid>/<string:public_key>')
def static_proxy(uid, public_key):
    """Serve static files."""
    file_path = os.path.join(working_dir, FILES_PREFIX, uid)
    app.logger.info('Processing file {}'.format(file_path))

    return send_from_directory(file_path, public_key)


# TODO: add a proper queue
@app.route('/process-block', methods=['POST'])
def process_block():
    """Process a new update from blockchain."""
    block_meta = request.get_json()
    app.logger.info("Received process request {}".format(block_meta))

    # TODO: move this processing to a separate thread
    user_id = block_meta['user_id']
    key_scopes = extract_by_key(block_meta['scopes'])

    app.logger.info("Triggering event to user {} with request {}".format(user_id, key_scopes))

    return jsonify({'message': 'Queued to process encode a file'})


# Run the server app
if __name__ == "__main__":
    app.debug = True
    app.run()
    app.run(debug=True)
