import firebase_admin
from firebase_admin import credentials, firestore, initialize_app

# initialize firestore db
cred = credentials.Certificate('firestorekey.json')
default_app = initialize_app(cred)
# the actial db
db = firestore.client()

# method to retrieve matches given a user id
def retrieve_matches(user_id):
    doc_ref = db.collection(u'users').document(user_id)
    doc = doc_ref.get()
    user_data = doc.to_dict()
    query = db.collection(u'users')
    # query = query.where(u'id', u'!=', user_id)
    # if data["roomgender"] == "No":
    #     query = query.where(u'gender', u'==', data["gender"])
    # query = query.where(u'lengthofstay', u'==', data["lengthofstay"])
    # query = query.where(u'university', u'==', data["university"])
    query = query.limit(2)
    docs = query.stream()
    matches = []
    for doc in docs:
        data = doc.to_dict()
        if not data["id"] == user_id and data["university"] == user_data["university"]:
            matches.append(doc.to_dict())
    doc_ref.update({"matches": matches})
    