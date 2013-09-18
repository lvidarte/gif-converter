import os
import string
import random

from flask import Flask, request, redirect, url_for, \
                  send_from_directory, render_template

from converter import convert_gif_to_png

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'uploads')
ALLOWED_EXTENSIONS = set(['gif'])


app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def id_generator():
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(4))

def create_random_dir():
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    while True:
        dirname = id_generator()
        path = os.path.join(UPLOAD_DIR, dirname)
        if not os.path.exists(path):
            os.makedirs(path)
            return dirname

@app.route('/<dirname>')
def show_animation(dirname):
    files = os.listdir(os.path.join(UPLOAD_DIR, dirname))
    gif_image = files.pop(files.index('image.gif'))
    png_image = files[0]
    return render_template('show_animation.html',
                           dirname=dirname,
                           gif_image=gif_image,
                           png_image=png_image)

@app.route('/uploads/<dirname>/<filename>')
def uploaded_file(dirname, filename):
    upload_dir = os.path.join(UPLOAD_DIR, dirname)
    return send_from_directory(upload_dir, filename)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            dirname = create_random_dir()
            upload_dir = os.path.join(UPLOAD_DIR, dirname)
            file.save(os.path.join(upload_dir, 'image.gif'))
            convert_gif_to_png(upload_dir, 'image.gif')
            return redirect(url_for('show_animation', dirname=dirname))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype="multipart/form-data">
        <p>
            <input type=file name=file>
            <input type=submit value=Upload>
    </form>
    '''


if __name__ == "__main__":
    app.run(debug=True)

