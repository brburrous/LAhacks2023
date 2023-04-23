import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    UPLOAD_FOLDER = os.path.join('app', 'static/uploads')
    
=======
>>>>>>> b06bffb (idk what i just did lol)
