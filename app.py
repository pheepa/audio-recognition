import os
from flask import Flask, flash, request, redirect, render_template
from tools import init_model, trasncribize
# from werkzeug.utils import secure_filename

app=Flask(__name__)

app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

path = os.getcwd()
# file Upload
# UPLOAD_FOLDER = os.path.join(path, 'data/')

# if not os.path.isdir(UPLOAD_FOLDER):
    # os.mkdir(UPLOAD_FOLDER)

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


ALLOWED_EXTENSIONS = set(['wav'])

model = init_model()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_file():
   if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            filename = file.filename
            # trans = trasncribize(model, file)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save('data/' + filename)
            trans = trasncribize(model, 'data/' + filename)
            flash(trans)
            return redirect('/')
        else:
            flash('Allowed file types are wav')
            return redirect(request.url)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)