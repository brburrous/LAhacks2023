from flask import render_template, request, session
from app import app
import boto3, json
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
 


# @app.route('/sign_s3/')
# def sign_s3():
#   S3_BUCKET = os.environ.get('S3_BUCKET')

#   file_name = request.args.get('file_name')
#   file_type = request.args.get('file_type')

#   s3 = boto3.client('s3')

#   presigned_post = s3.generate_presigned_post(
#     Bucket = S3_BUCKET,
#     Key = file_name,
#     Fields = {"acl": "public-read", "Content-Type": file_type},
#     Conditions = [
#       {"acl": "public-read"},
#       {"Content-Type": file_type}
#     ],
#     ExpiresIn = 3600
#   )

#   return json.dumps({
#     'data': presigned_post,
#     'url': 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, file_name)
#   })




