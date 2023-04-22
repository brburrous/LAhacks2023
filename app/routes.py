from flask import render_template, request, session
from app import app
import os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


@app.route('/')
@app.route('/index')
def index():
    return render_template('images.html')


@app.route('/',  methods=("POST", "GET"))
def uploadFiles():
    if request.method == 'POST':
        # Upload file flask
        uploaded_img = request.files['uploaded-file']
        # Extracting uploaded data file name
        img_filename = secure_filename(uploaded_img.filename)
        # Upload file to database (defined uploaded folder in static path)
        print(app.config["UPLOAD_FOLDER"])
        print("foo")
        uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
        # Storing uploaded file path in flask session
        session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
        session['uploaded_img_file_name'] = os.path.join("uploads", img_filename)
 
    return render_template('images2.html')

@app.route('/show_image')
def displayImage():
    # Retrieving uploaded file path from session
    # img_file_path = session.get('uploaded_img_file_path', None)
    img_file_name = session.get('uploaded_img_file_name', None)
    # Display image in Flask application web page
    return render_template('show_image.html', user_image = img_file_name)
 