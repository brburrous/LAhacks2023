import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('firebase_key.json')
app = firebase_admin.initialize_app(cred)

db = firestore.client() 

def addName(db, url):
    db.collection(u'img_urls').add({
        u'bmj': url,
        u'processed': False
    })

def getNames(db):
    ref = db.collection(u'img_urls') 
    unprocessed = ref.where(u'processed', u'==', False)
    return list(map(lambda x: (x.id, x.to_dict()), unprocessed.stream()))

names = getNames(db)

def updateDoc(db, docID):
    doc_ref = db.collection(u'img_urls').document(docID)

    doc_ref.set({
        u'newUrl': u"ffffooooooo",
        u'processed': True
    }, merge=True)


name = names[1][0]