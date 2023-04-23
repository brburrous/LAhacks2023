from flask import render_template, request, session
from app import app
import boto3, json
import os
from werkzeug.utils import secure_filename
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore



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
        print(f"memetype lol: {uploaded_img.mimetype}")
        # Extracting uploaded data file name
        img_filename = secure_filename(uploaded_img.filename)
        # Upload file to database (defined uploaded folder in static path)
        print(app.config["UPLOAD_FOLDER"])
        print("foo")
        uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
        # Storing uploaded file path in flask session
        session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
        session['uploaded_img_file_name'] = os.path.join("uploads", img_filename)
        
        s3 = boto3.client("s3")
        s3.upload_file(
            Filename=session['uploaded_img_file_path'],
            Bucket="lahacks2023-ky-austin-riley-brian",
            Key=img_filename,
            ExtraArgs={
                'ContentType':uploaded_img.mimetype
            }
        ) 
    return render_template('images2.html')

@app.route('/show_image')
def displayImage():
    # Retrieving uploaded file path from session
    # img_file_path = session.get('uploaded_img_file_path', None)
    img_file_name = session.get('uploaded_img_file_name', None)
    # Display image in Flask application web page
    return render_template('show_image.html', user_image = img_file_name)
 

@app.route('/firebase')
def add2Firebase():
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate('firebase_key.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client() 
doc_ref = db.collection(u'users').document(u'alovelace')
doc_ref.set({
    u'first': u'Ada',
    u'last': u'Lovelace',
    u'born': 1815
})
    

def addName(name):
    cred = credentials.Certificate('firebase_key.json')

    app = firebase_admin.initialize_app(cred)

    db = firestore.client() 
    doc_ref = db.collection(u'users').document(name)
    doc_ref.set({
        u'first': name,
        u'last': u'Lovelace',
        u'born': 1815
    })