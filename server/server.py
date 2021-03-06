"""Simple API to serve encrypted files to Providers."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import os

import psycopg2

from flask import Flask, jsonify, send_from_directory, request, g

from utils import extract_by_key

app = Flask(__name__)
working_dir = os.getcwd()
FILES_PREFIX = 'user_files'


def get_db():
    """Open a new database connection if there is none yet for the current application context."""
    if not hasattr(g, 'db_connection'):
        g.db_connection = psycopg2.connect("dbname=postgres user=khomenkos")
    return g.db_connection


@app.teardown_appcontext
def close_db(error):
    """Close the database again at the end of the request."""
    if hasattr(g, 'db_connection'):
        g.db_connection.close()


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
@app.route('/user/<string:uid>/<string:public_key>', methods=['POST'])
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

    db_connection = get_db()
    cursor = db_connection.cursor()
    cursor.execute("""INSERT INTO t_requests (a_uid, a_request)
                        VALUES (%s, %s)""", (user_id, json.dumps(key_scopes)))
    db_connection.commit()
    app.logger.info("Added an event to user {} with request {}".format(user_id, key_scopes))

    return jsonify({'message': 'Queued to process encode a file'})


@app.route('/user/<string:uid>/requests', methods=['GET'])
def get_requests(uid):
    """Return requests for user."""
    db_connection = get_db()
    cursor = db_connection.cursor()
    cursor.execute("SELECT a_request FROM t_requests WHERE a_uid = (%s)", (uid, ))

    data = cursor.fetchone()

    if data:
        return jsonify({'request': data})
    else:
        return jsonify({'message': 'No requests yet'})


@app.route('/user/<string:uid>/processed', methods=['GET'])
def mark_processed(uid):
    """Mark user request as processed."""
    db_connection = get_db()
    cursor = db_connection.cursor()
    cursor.execute("DELETE FROM t_requests WHERE a_uid = (%s)", (uid, ))

    db_connection.commit()

    return jsonify({'message': 'Request was removed'})


# Run the server app
if __name__ == "__main__":
    app.debug = True
    app.config['UPLOAD_FOLDER'] = FILES_PREFIX
    app.run()
    app.run(debug=True)
