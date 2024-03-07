from optparse import OptionParser
from os.path import isfile, join
import json

from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

from PIL import Image
import pytesseract


UPLOAD_FOLDER = '.'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def hello():
    return "<p>Screen Verifier!</p>"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/verify', methods=['GET', 'POST'])
def upload_file():
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
            filepath = join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            sentences = json.loads(request.form.get('sentences', None))
            missing = screenverifier(filepath, sentences)
            return {
                'missing': missing
            }
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=text name=sentences>
      <input type=submit value=Upload>
    </form>
    '''

def screenverifier(screenpath, args):
    text = pytesseract.image_to_string(Image.open(screenpath))
    missing = []

    for arg in args:
        if arg not in text:
            missing.append(arg)
    
    return missing


"""
def main():
    usage = "python3 screenverifier.py --screenpath <path to file with screenshot> 'text1' 'text2' ... 'textN'"

    parser = OptionParser(usage)
    parser.add_option("-s", "--screenpath", dest="screenpath", help="screenpath")

    (options, args) = parser.parse_args()

    if not options.screenpath:
        parser.error('screenpath is missing')
    if not len(args):
        parser.error('no text specified')
    
    if not isfile(options.screenpath):
        print("Input file does not exist")
        exit(-1)
    
    screenverifier(options.screenpath, args)

if __name__ == "__main__":
    main()
"""