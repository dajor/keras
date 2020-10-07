__author__ = 'vitor'

from flask.globals import request
from flask import render_template
from . import main
import os
from werkzeug.utils import secure_filename

from pathlib import Path
import predict as pd

@main.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return

        target = os.path.join(get_project_root(), "UploadedFiles")
        if not os.path.isdir(target):
            os.mkdir(target)

        for file in request.files.getlist("file"):
            filename = secure_filename(file.filename)
            destination = '/'.join([target, filename])
            file.save(destination)

            pre_dir = os.path.join(get_project_root(), 'predicts')
            #pd.make_predictions(destination, 'invoice_number', pre_dir)
            pd.make_predictions(destination, 'vendor_name', pre_dir)
            #pd.make_predictions(destination, 'invoice_date', pre_dir)
            #pd.make_predictions(destination, 'tax_amount', pre_dir)
            #pd.make_predictions(destination, 'total_amount', pre_dir)


    return render_template('upload.html')


def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent

