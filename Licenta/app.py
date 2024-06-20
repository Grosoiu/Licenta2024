from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import os
import subprocess
from pyngrok import ngrok

app = Flask(__name__)

# Set your paths here
UPLOAD_FOLDER = 'C:/Users/Grosi/Licenta2024/Licenta/main/in_files'
OUTPUT_FOLDER = 'C:/Users/Grosi/Licenta2024/Licenta/main/out_files'
EXECUTABLES = {
    'reverb': 'C:/Users/Grosi/Licenta2024/Licenta/main/reverb_audio.exe',
    'shift': 'C:/Users/Grosi/Licenta2024/Licenta/main/shift_audio.exe',
    'stretch': 'C:/Users/Grosi/Licenta2024/Licenta/main/stretch_audio.exe',
    'tnnr': 'C:/Users/Grosi/Licenta2024/Licenta/main/executabil.exe',
    'convert': 'C:/Users/Grosi/Licenta2024/Licenta/main/convert.exe'
}
ALLOWED_EXTENSIONS = {'mp3', 'wav'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/upload/<action>', methods=['GET', 'POST'])
def upload_file(action):
    if action not in EXECUTABLES:
        return redirect(url_for('home'))
    if request.method == 'POST':
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = 'fisier.mp3'  # Overwrite the existing input file
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            # Handle slider values
            command = [EXECUTABLES[action]]
            output_filename = 'fisier'
            if action == 'stretch':
                stretch_value = request.form.get('stretch-value', '1')
                command.append(stretch_value)
            elif action == 'shift':
                shift_value = request.form.get('shift-value', '0')
                command.append(shift_value)
            elif action == 'convert':
                filetype = request.form.get('filetype', 'wav')
                command.append(filetype)
                output_filename += f'.{filetype}'
            subprocess.run(command, shell=True)
            return redirect(url_for('display_files', action=action, output_filename=output_filename))
    return render_template('upload.html', action=action)


@app.route('/outputs', methods=['GET'])
def display_files():
    action = request.args.get('action', 'reverb')
    output_filename = request.args.get('output_filename', 'fisier.wav')
    files = os.listdir(OUTPUT_FOLDER)
    return render_template('display_files.html', files=files, action=action, output_filename=output_filename)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route('/outputs/<filename>')
def output_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)


if __name__ == '__main__':
    app.run(debug=True)
