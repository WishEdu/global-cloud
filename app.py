from os import path, mkdir, remove

import flask
from flask_cors import CORS

from configs import ASSETS_DIR, MAIN_ROUTE, PORT
from utils import create_unique_id
import db


app = flask.Flask(__name__)
CORS(app)


@app.post(MAIN_ROUTE)
def handle_file():
    file = flask.request.files['file']

    file_owner = flask.request.args["file_owner"]
    file_owner_id = flask.request.args["file_owner_id"]
    file_type = flask.request.args["file_type"]

    dir_url = path.join(file_owner, file_owner_id, file_type)
    unique_id = create_unique_id(file.filename, file_owner, file_owner_id)
    file_name = f'{unique_id}.{file.filename.split(".")[-1]}'

    url = path.join(dir_url, file_name)
    
    if not path.isdir(path_ := path.join(ASSETS_DIR, file_owner)):
        mkdir(path_)
    if not path.isdir(path_ := path.join(ASSETS_DIR, file_owner, file_owner_id)):
        mkdir(path_)
    if not path.isdir(path_ := path.join(ASSETS_DIR, dir_url)):
        mkdir(path_)

    file_id = str(db.add_file(file_owner, file_owner_id, file_type, file_name)['id'])
    file.save(path.join(ASSETS_DIR, url))

    return flask.jsonify({"file_id": file_id}), 200


@app.route(MAIN_ROUTE, methods=['GET', 'DELETE'])
def get_or_delete_file_url_by_id():
    file_id = flask.request.args['file_id']
    data = db.get_by_file_id(file_id)
    if data is None:
        return flask.jsonify({'errorMessage': 'No file with such file_id'}), 400
    if data == -1:
        return flask.jsonify({'errorMessage': 'SQL error'}), 500
    url = path.join(data['owner_type'], str(data['owner_id']), data['file_type'], data['file_name'])

    if not path.isfile(path_ := path.join(ASSETS_DIR, url)):
        return flask.jsonify({'errorMessage': 'No such file'}), 500
    
    if flask.request.method == 'GET':
        return flask.jsonify({"file_endpoint": '/assets/' + url}), 200

    if flask.request.method == 'DELETE':
        delete_code = db.delete_by_file_id(file_id)
        if delete_code == -1:
            return flask.jsonify({'errorMessage': 'SQL error'}), 500
        remove(path_)
        return flask.jsonify({"status": "OK"}), 200
    

@app.get(MAIN_ROUTE+'/avalogo')
def get_user_avatar_or_group_logo():
    owner_type = flask.request.args['owner_type']
    owner_id = flask.request.args['owner_id']

    data = db.get_user_avatar_or_group_logo(owner_type, owner_id)
    if data is None:
        return flask.jsonify({'errorMessage': 'No such owner'})
    if data == -1:
        return flask.jsonify({'errorMessage': 'SQL error'}), 500
    
    url = path.join(owner_type, str(owner_id), data['file_type'], data['file_name'])
    if not path.isfile(path.join(ASSETS_DIR, url)):
        return flask.jsonify({'errorMessage': 'No such file'}), 500
    
    return flask.jsonify({"file_endpoint": path.join('/assets', url)}), 200


if __name__ == '__main__':
    app.run(host='localhost', port=PORT, debug=True)
