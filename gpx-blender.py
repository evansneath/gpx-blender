#!/usr/bin/python

from flask import *
import os
import string
import random

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['UPLOAD_DIR'] = os.getcwd() + '/static/uploads'
app.config['FILENAME_SIZE'] = 6

def is_gpx(filename):
    # Determine if a file has the .gpx extension
    return filename.rsplit('.', 1)[1] == 'gpx'


@app.route('/')
def index():
    return redirect(url_for('upload'))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        error = None 

        # Get all files from the form
        gpx_file_1 = request.files['gpx_file_1']
        gpx_file_2 = request.files['gpx_file_2']

        if not gpx_file_1 or not gpx_file_2:
            error = 'Both files must be chosen for upload'
        elif not is_gpx(gpx_file_1.filename) or not is_gpx(gpx_file_2.filename):
            error = 'Uploaded files must be of type .gpx'

        if error is None:
            # Everything is ok, parsing the files
            gpx_head = gpx_file_1.read().split('</trk>')[0]
            gpx_tail = gpx_file_2.read().split('<trk>')[1]
            # Combine the parsed head and tail of the gpx route
            gpx_concat = gpx_head + gpx_tail

            # File is now created, saving to drive with a random filename.
            chars = string.ascii_uppercase + string.digits
            filename = ''.join(random.choice(chars) for x in range(app.config['FILENAME_SIZE'])) + '.gpx'
            filepath = os.path.join(app.config['UPLOAD_DIR'], filename)
            fstream = open(filepath, 'w+')

            fstream.write(gpx_concat)
            
            return render_template('success.html', file_download=filename)
        else:
            return render_template('upload.html', error=error)
    else:
        return render_template('upload.html')


if __name__ == '__main__':
    app.run(debug=True)
