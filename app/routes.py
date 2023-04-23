from flask import render_template, request, session
from app import app
import boto3, json
import os
from werkzeug.utils import secure_filename

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime


cred = credentials.Certificate('firebase_key.json')
firebase_admin.initialize_app(cred)

db = firestore.client() 


UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def addName(db, url):
    db.collection(u'img_urls').add({
        u'bmj': url,
        u'processed': False,
        u'date':datetime.now()
    })


@app.route('/')
@app.route('/index')
def index():
    return render_template('style_selection.html')


@app.route('/upload',  methods=("POST", "GET"))
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
        url = f"https://lahacks2023-ky-austin-riley-brian.s3.us-west-1.amazonaws.com/{img_filename}"
        addName(db, url)
        img_file_name = session.get('uploaded_img_file_name', None)
        print(request.args)
        print(request.form.get("fullDesc"))
        title = request.form.get("fullTitle")
        desc = request.form.get("fullDesc")
        routeNum = int(request.form.get("number"))
        print(routeNum)
    return render_template('narrative_builder2.html', title=title, description=desc, route_num=routeNum, img_file_name=img_file_name)

@app.route('/show_image')
def displayImage():
    # Retrieving uploaded file path from session
    # img_file_path = session.get('uploaded_img_file_path', None)
    img_file_name = session.get('uploaded_img_file_name', None)
    # Display image in Flask application web page
    return render_template('show_image.html', user_image = img_file_name)
 

@app.route('/narrative.builder1')
def narrative_builder1():
    title = 'Part 1: Call to Adventure'
    description = 'Upload an image that signifies the beginning of your adventure'
    return render_template('narrative_builder.html', title=title, description=description, route_num=1)

@app.route('/narrative.builder2')
def narrative_builder2():
    title = 'Part 2: The Crossing of the First Threshold'
    description = 'This is the point where the hero actually crosses into the field of adventure, leaving the known limits of their world and venturing into an unknown and dangerous realm where the rules and limits are unknown'
    return render_template('narrative_builder.html', title=title, description=description, route_num=2)

@app.route('/narrative.builder3')
def narrative_builder3():
    title = 'Part 3: The Road of Trials'
    description = 'The road of trials is a series of tests that the hero must undergo to begin the transformation. Often the hero fails one or more of these tests. Eventually, the hero will overcome these trials and move on to the next step.'
    return render_template('narrative_builder.html', title=title, description=description, route_num=3)

@app.route('/narrative.builder4')
def narrative_builder4():
    title = 'Part 4: Ordeal/Abyss'
    description = 'The hero experiences a major hurdle or obstacle, such as a life-or-death crisis. They must come face to face with their weaknesses and must overcome them. This will be something the hero barely manages to accomplish'
    return render_template('narrative_builder.html', title=title, description=description, route_num=4)

@app.route('/narrative.builder5')
def narrative_builder5():
    title = 'Part 5: Reward'
    description = 'After surviving death, the hero earns a reward or accomplishes their goal. This is a moment of great success in the story. The hero is a changed person now, though they may not fully realize the extent of the change in their continued focus on the matter at hand.'
    return render_template('narrative_builder.html', title=title, description=description, route_num=5)

@app.route('/narrative.builder6')
def narrative_builder6():
    title = 'Part 6: Return with Elixir'
    description = 'The hero brings their knowledge or the "elixir" back to the ordinary world, where they apply it to help all who remain there. This is the true reward for the journey and transformation'
    return render_template('narrative_builder.html', title=title, description=description, route_num=6)

@app.route('/your.story')
def your_story():
    return render_template('your_story.html')

@app.route('/loading')
def loading():
    return render_template('loading.html')
