"""Simple API to serve encrypted files to Providers."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from flask import Flask, jsonify, send_from_directory
import json
import os

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
    print(file_path)

    return send_from_directory(file_path, public_key)

# Run the server app
if __name__ == "__main__":
    app.debug = True
    app.run()
    app.run(debug=True)
