from flask import Flask, request, redirect, url_for, jsonify, render_template
import os

import firebase_admin
from firebase_admin import credentials, firestore, initialize_app

# initialize firestore db
cred = credentials.Certificate('firestorekey.json')
default_app = initialize_app(cred)
# the actial db
db = firestore.client()

# method to retrieve matches given a user id
# def retrieve_matches(user_id):
    # TODO

# flask app
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/result/<user_id>")
def result(user_id):
    doc_ref = db.collection(u'test').document(user_id)
    doc = doc_ref.get()
    age_of_user = doc.to_dict()["age"]
    return render_template("result.html", age=age_of_user)

@app.route("/form", methods=["POST", "GET"])
def form():
    if request.method == "POST":
        user_id = request.form["nm"]
        user_name = user_id
        user_age = request.form["age"]
        doc_ref = db.collection(u'test').document(user_id)
        doc_ref.set({
            u'name': user_name,
            u'age': user_age
        })
        return redirect(url_for("result", user_id=user_id))
        # method to put data into database
    else:
          return render_template("form.html")

if __name__ == "__main__":
    app.run(debug=True)