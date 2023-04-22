import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    UPLOAD_FOLDER = os.path.join('app', 'static/uploads')
    AWS_ACCESS_KEY_ID='AKIASVLUVDCSJ7TS36GP'
    AWS_SECRET_ACCESS_KEY='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'
    S3_BUCKET='lahacks2023-ky-austin-riley-brian'
