from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import os
import subprocess

app = Flask(__name__)

# Set your paths here
UPLOAD_FOLDER = 'C:/Users/Grosi/Desktop/Licenta/main/in_files'
OUTPUT_FOLDER = 'C:/Users/Grosi/Desktop/Licenta/main/out_files'
EXECUTABLE_PATH = 'C:/Users/Grosi/Desktop/Licenta/main/executabil.exe'
ALLOWED_EXTENSIONS = {'mp3', 'wav'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an empty file without a filename.
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = 'fisier.mp3'  # Overwrite the existing input file
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            # Run the executable
            subprocess.run(EXECUTABLE_PATH, shell=True)
            return redirect(url_for('display_files'))
    return render_template('index.html')


@app.route('/outputs', methods=['GET'])
def display_files():
    files = os.listdir(OUTPUT_FOLDER)
    return render_template('display_files.html', files=files)


@app.route('/outputs/<filename>')
def uploaded_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)


if __name__ == '__main__':
    app.run(debug=True)
