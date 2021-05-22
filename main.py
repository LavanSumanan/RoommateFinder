from flask import Flask, request, redirect, url_for, jsonify
import os
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app

# initialize firestore db
cred = credentials.Certificate('firestorekey.json')
default_app = initialize_app(cred)
# the actial db
db = firestore.client()

# flask app
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/form", methods=["POST", "GET"])
def form():
    if request.method == "POST":
        print(request.form.to_dict())
        user_name = request.form["nm"]
        user_age = request.form["age"]
        doc_ref = db.collection(u'test').document(u'firstuser')
        doc_ref.set({
            u'name': user_name,
            u'age': user_age
        })
        # method to put data into database
    else:
          return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True)