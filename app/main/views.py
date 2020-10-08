__author__ = 'vitor'

import json
import os
from pathlib import Path
from urllib.parse import urlparse

import predict as pd
from flask import Flask, jsonify, render_template,send_file
from flask.globals import request
from pdf2image import convert_from_path
from werkzeug.utils import secure_filename

from . import main

uploads_dirname = 'uploaded_files'
thumbs_dirname = 'thumbs_files'

@main.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return
        resp = {}
        target = os.path.join(get_project_root(), uploads_dirname)

        if not os.path.isdir(target):
            os.mkdir(target)

        for file in request.files.getlist("file"):
            filename = secure_filename(file.filename)
            destination = '/'.join([target, filename])
            file.save(destination)

            error = False
            try:
                extract_data(destination)
                #pass
            except Exception:
                error = True
                resp['data'] = {'error':1, 'message':'Error extracting data.' }

            if not error:
                try:
                    resp['data'] = get_extracted_data(destination)
                except Exception:
                    error = True
                    resp['data'] = {'error':1, 'message':'Error loading extracted data file.' }              

        resp['status_code'] = 200
        json_object = json.dumps(resp, indent=4)
        return json_object

    return render_template('upload.html')

@main.route('/temp', methods=['GET'])
def temp():
    return render_template('temp.html')


@main.route('/image/<path>', methods=['GET'])
def images(path):
    a = urlparse(path)
    pdf_dir = os.path.join(get_project_root(), uploads_dirname)
    imgs_dir = os.path.join(get_project_root(), thumbs_dirname)

    filename = os.path.basename(a.path)
    if not filename.endswith('.pdf'):
        filename = os.path.splitext(filename)[0]

    if not os.path.isdir(imgs_dir):
            os.mkdir(imgs_dir)

    if not os.path.isdir(pdf_dir):
            os.mkdir(pdf_dir)

    pdf_path = os.path.join(pdf_dir, filename+'.pdf')
    img_path = os.path.join(imgs_dir, filename+'.JPEG')

    if not os.path.isfile(img_path):
        pages = convert_from_path(pdf_path, 500)
        for page in pages:
            page.save(img_path, 'JPEG')
            break

    return send_file(img_path, mimetype='image/jpeg')


def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent


def extract_data(filepath):
    predictions_dir = os.path.join(get_project_root(), 'predictions')

    pd.make_predictions(filepath, 'invoice_number', predictions_dir)
    pd.make_predictions(filepath, 'vendor_name', predictions_dir)
    pd.make_predictions(filepath, 'invoice_date', predictions_dir)
    pd.make_predictions(filepath, 'tax_amount', predictions_dir)
    pd.make_predictions(filepath, 'total_amount', predictions_dir)


def get_extracted_data(filepath):
    predictions_dir = os.path.join(get_project_root(), 'predictions')
    filename_wo_ext = Path(filepath).stem
    #filename_wo_ext = '4644_001'
    predictions_file = os.path.join(predictions_dir, filename_wo_ext + '.json')
    with open(predictions_file) as json_file:
        data = json.load(json_file)
        data['filename'] = filename_wo_ext
        return data
