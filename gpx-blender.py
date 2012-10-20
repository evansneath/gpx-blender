#!/usr/bin/python

from flask import *
import os
import string
import random

# Instantiate Flask API object, define config options.
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['UPLOAD_DIR'] = os.path.join(os.getcwd(), 'uploads')
app.config['FILENAME_LEN'] = 6


def has_gpx_ext(file):
    # Determine if a file has the .gpx extension.
    return file.filename.rsplit('.', 1)[1] == 'gpx'


def is_valid_gpx(file_data):
    # Determine if a file is a valid gpx file.
    return '<trk>' in file_data and '</trk>' in file_data


def get_random_str(length):
    # Returns a random string of uppercase characters and digits.
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for x in range(length))


def download_file(filename):
    return send_from_directory(app.config['UPLOAD_DIR'], filename)


@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        error = None 

        # Get all files from the form.
        file1 = request.files['gpx_file_1']
        file2 = request.files['gpx_file_2']

        # Detect if the inputted files exist and are valid.
        if not file1 or not file2:
            error = 'Both files must be chosen for upload'
            return render_template('upload.html', error=error)
        elif not has_gpx_ext(file1) or not has_gpx_ext(file2):
            error = 'Uploaded files must be of type .gpx'
            return render_template('upload.html', error=error)

        # The files have the possibility of being valid. Read the data.
        file1_data = file1.read()
        file2_data = file2.read()

        # Close the files for reading.
        file1.close()
        file2.close()

        # See if the data matches a parsable format.
        if not is_valid_gpx(file1_data) or not is_valid_gpx(file2_data):
            error = 'Uploaded files are not valid .gpx files'
            return render_template('upload.html', error=error)

        # Everything is ok, parsing the files.
        file1_head = file1_data.split('</trk>')[0]
        file2_tail = file2_data.split('<trk>')[1]

        # Combine the parsed head and tail of the gpx route.
        gpx_concat = file1_head + file2_tail

        # File is now created, saving to drive with a random filename.
        chars = string.ascii_uppercase + string.digits
        filename = get_random_str(app.config['FILENAME_LEN']) + '.gpx'
        filepath = os.path.join(app.config['UPLOAD_DIR'], filename)

        # If the upload directory doesn't exist, create one.
        if not os.path.exists(app.config['UPLOAD_DIR']):
            os.makedirs(app.config['UPLOAD_DIR'])

        # Open the file for writing and write all data.
        fstream = open(filepath, 'w+')
        fstream.write(gpx_concat)

        return render_template('success.html', download=filepath,
                               filename=filename)
    else:
        return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)

