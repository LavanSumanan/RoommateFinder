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
    query = db.collection(u'users').where(u'id', u'!=', user_id)
    # if user_data["roomgender"] == "No":
    #     query = query.where(u'gender', u'==', user_data["gender"])
    # query = query.where(u'lengthofstay', u'==', user_data["lengthofstay"])
    # query = query.where(u'university', u'==', user_data["university"])
    query = query.limit(3)
    docs = query.stream()
    matches = []
    for doc in docs:
        matches.append(doc.to_dict())
    doc_ref.update({"matches": matches})