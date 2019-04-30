from flask import Flask, request, send_from_directory, jsonify

import os
import json
import sys

import wand.image

# Extend path to load Froala Editor library from outside the server.
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)) + "/../")

from froala_editor import File, Image, Video, S3
from froala_editor import FlaskAdapter

# Create public directory at startup.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
publicDirectory = os.path.join(BASE_DIR, 'public')
if not os.path.exists(publicDirectory):
    os.makedirs(publicDirectory)

app = Flask(__name__, static_url_path='')

@app.route('/')
def get_main_html():
    return send_from_directory('..', 'common/index.html')

@app.route('/public/<path:path>')
def get_public(path):
    return send_from_directory('public/', path)

@app.route('/static/<path:path>')
def get_static(path):
    return send_from_directory('../', path)



@app.route('/upload_file', methods=['POST'])
def upload_file():
    options = {
        'validation': None
    }
    try:
        response = File.upload(FlaskAdapter(request), '/public/', options)
    except Exception:
        response = {'error': str(sys.exc_info()[1])}
    return json.dumps(response)

@app.route('/upload_file_validation', methods=['POST'])
def upload_file_validation():

    def validation(filePath, mimetype):
        size = os.path.getsize(filePath)
        if size > 10 * 1024 * 1024:
            return False
        return True

    options = {
        'fieldname': 'myFile',
        'validation': validation
    }
    try:
        response = File.upload(FlaskAdapter(request), '/public/', options)
    except Exception:
        response = {'error': str(sys.exc_info()[1])}
    return json.dumps(response)

@app.route('/upload_image', methods=['POST'])
def upload_image():
    try:
        response = Image.upload(FlaskAdapter(request), '/public/')
    except Exception:
        response = {'error': str(sys.exc_info()[1])}
    return json.dumps(response)

@app.route('/upload_image_validation', methods=['POST'])
def upload_image_validation():

    def validation(filePath, mimetype):
        with wand.image.Image(filename=filePath) as img:
            if img.width != img.height:
                return False
            return True

    options = {
        'fieldname': 'myImage',
        'validation': validation
    }
    try:
        response = Image.upload(FlaskAdapter(request), '/public/', options)
    except Exception:
        response = {'error': str(sys.exc_info()[1])}
    return json.dumps(response)

@app.route('/upload_image_resize', methods=['POST'])
def upload_image_resize():
    options = {
      'resize': '300x300'
    }
    try:
        response = Image.upload(FlaskAdapter(request), '/public/', options)
    except Exception:
        response = {'error': str(sys.exc_info()[1])}
    return json.dumps(response)


@app.route('/upload_video', methods=['POST'])
def upload_video():
    try:
        response = Video.upload(FlaskAdapter(request), '/public/')
    except Exception:
        response = {'error': str(sys.exc_info()[1])}
    return json.dumps(response)

@app.route('/upload_video_validation', methods=['POST'])
def upload_video_validation():

    def validation(filePath, mimetype):
        size = os.path.getsize(filePath)
        if size > 50 * 1024 * 1024:
            return False
        return True

    options = {
        'fieldname': 'myFile',
        'validation': validation
    }
    try:
        response = Video.upload(FlaskAdapter(request), '/public/', options)
    except Exception:
        response = {'error': str(sys.exc_info()[1])}
    return json.dumps(response)

@app.route('/delete_file', methods=['POST'])
def delete_file():
    src = request.form.get('src')
    try:
      File.delete(src)
      return json.dumps('ok')
    except:
      raise Exception('Could not delete file')

@app.route('/delete_image', methods=['POST'])
def delete_image():
    src = request.form.get('src')
    try:
      Image.delete(src)
      return json.dumps('ok')
    except:
      raise Exception('Could not delete image')

@app.route('/load_images')
def load_images():
    try:
        response = Image.list('/public/')
    except Exception:
        response = {'error': str(sys.exc_info()[1])}
    return json.dumps(response)

@app.route('/amazon_hash')
def amazon_hash():
    config = {
        'bucket': os.environ['AWS_BUCKET'],
        'region': os.environ['AWS_REGION'],
        'keyStart': os.environ['AWS_KEY_START'],
        'acl': os.environ['AWS_ACL'],
        'accessKey': os.environ['AWS_ACCESS_KEY'],
        'secretKey': os.environ['AWS_SECRET_ACCESS_KEY']
    }
    try:
        response = S3.getHash(config)
    except Exception:
        response = {'error': str(sys.exc_info()[1])}
    return jsonify(**response)
