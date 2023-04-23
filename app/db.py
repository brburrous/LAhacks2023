import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import boto3

from midjourney import invoke_midjourney

from dotenv import load_dotenv
import os
import time

cred = credentials.Certificate('firebase_key.json')
app = firebase_admin.initialize_app(cred)

db = firestore.client() 

load_dotenv('keys.env')
BUCKET_NAME = 's3-bark'
CURRENT_URL = ''

s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
)

def addName(db, name, url):
    db.collection(u'img_urls').add({
        u'name': name,
        u'bmj': url,
        u'processed': False
    })

def get_unprocessed_names(db):
    ref = db.collection(u'img_urls') 
    unprocessed = ref.where(u'processed', u'==', False)
    return list(map(lambda x: (x.id, x.to_dict()), unprocessed.stream()))

def update_db(db, docID, url):
    doc_ref = db.collection(u'img_urls').document(docID)

    doc_ref.set({
        u'newUrl': url,
        u'processed': True
    }, merge=True)


def process_images(db, names):
    global CURRENT_URL
    for name in names:
        colID = name[0]
        
        url = name[1]['bmj']
        #prompt = name[1]['prompt']
        prompt = 'under the red sea with starfish'
        #invoke autopygui script
        invoke_midjourney(url, prompt)
        print(f'{url} :::::: {prompt}')

        # wait to grab url data
        CURRENT_URL = wait_until_new_url()

        update_db(db, colID, CURRENT_URL)

def wait_until_new_url():
    urls_file = open('urls.txt', 'r')
    urls = urls_file.readlines()

    while len(urls) == 0:
        print('Waiting for at least 1 url to be added')
        time.sleep(1)
    while urls[len(urls)-1] == CURRENT_URL:
        print('waiting for new url')
        time.sleep(1)

    return urls[len(urls)-1]


while True:
    unprocessed_names = get_unprocessed_names(db)
    if len(unprocessed_names) > 0:
        process_images(db, unprocessed_names)
    time.sleep(1)



    