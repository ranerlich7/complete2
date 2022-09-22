import os
from flask import Blueprint, Flask, flash, render_template, request, redirect, send_from_directory, url_for
from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

upload_bp = Blueprint('file', __name__, url_prefix='/file')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/', methods=['GET', 'POST'])
def upload_file():
    from app.main import app
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('file.download_file', name=filename))
    return render_template('upload.html')


@upload_bp.route('/uploads/<name>')
def download_file(name):
    from app.main import app
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)