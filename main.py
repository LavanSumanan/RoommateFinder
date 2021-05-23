# ---------------------------------------------imports---------------------------------------------
from flask import Flask, request, redirect, url_for, jsonify, render_template
import os
from database import db, retrieve_matches
# ----------------------------------------------pages----------------------------------------------
message = "Find your Dioscuri!"

# arrays for points
bedtime = ["", "-1","7","3","12","10"]
waketime = ["","12+","12","10","8","6"]
noise_level = ["","Loud","Normal","Quiet"]
party = ["","Always","Often","Sometimes","Never"]

# flask app
app = Flask(__name__)

# home page
@app.route("/")
def home():
    global message
    message = "Find your Dioscuri!"
    return render_template("index.html")

@app.route("/profiles")
def profiles():
    global message
    message = "Find your Dioscuri!"
    return render_template("profiles.html")

# form page
@app.route("/form", methods=["POST", "GET"])
def form():
    # user has submitted form and data needs to be entered into database
    if request.method == "POST":
        user_name = request.form["name"]
        user_gender = request.form.get("gender")
        user_room_gender = request.form.get("roomgender")
        user_length_of_stay = request.form.get("lengthofstay")
        user_university = request.form.get("university")
        user_major = request.form.get("major")
        user_interests = request.form.getlist("interests")
        user_party = request.form.get("party")
        user_bedtime = request.form.get("bedtime")
        user_waketime = request.form.get("waketime")
        user_noise_level = request.form.get("noiselevel")
        user_neatness = request.form["neatness"]
        user_id = request.form["username"]
        user_password = request.form["password"]
        user_email = request.form["email"]
        
        user_score = int(user_neatness)
        user_score += waketime.index(user_waketime)
        user_score += bedtime.index(user_bedtime)
        user_score += party.index(user_party)
        user_score += noise_level.index(user_noise_level)
        print(f"-----------------user score = {user_score}-------------------")
        user_personality = ""
        if user_score >= 5 and user_score <= 9:
            user_personality = "Socialite"
        elif user_score >=10 and user_score <= 15:
            user_personality = "Juggler"
        elif user_score >= 16 and user_score <= 20:
            user_personality = "Equalizer"
        elif user_score >= 21 and user_score <= 25:
            user_personality = "Wallflower"
        
        doc_ref = db.collection(u'users').document(user_id)
        doc = doc_ref.get()
        if doc.exists:
            global message
            message = "That username is taken! Try again."
            return redirect(url_for("form"))
        else:
            message = "Find your Dioscuri!"
            doc_ref.set({
                u'name': user_name,
                u'gender': user_gender,
                u'roomgender': user_room_gender,
                u'lengthofstay': user_length_of_stay,
                u'university': user_university,
                u'major': user_major,
                u'interests': user_interests,
                u'neatness': user_neatness,
                u'party': user_party,
                u'bedtime': user_bedtime,
                u'waketime': user_waketime,
                u'noiselevel': user_noise_level,
                u'id': user_id,
                u'password': user_password,
                u'email': user_email,
                u'personality': user_personality,
                u'score': user_score,
                u'matches': []
            })
        return redirect(url_for("result", user_id=user_id))
    # user is viewing the form and filling it
    else:
        return render_template("form.html", message=message)

# results page
@app.route("/result/<user_id>")
def result(user_id):
    global message
    message = "Find your Dioscuri!"
    retrieve_matches(user_id)
    data = db.collection(u'users').document(user_id).get().to_dict()
    return render_template("result.html", elements=[data["personality"], data["matches"]])

if __name__ == "__main__":
    app.run(debug=True)