import os
from flask import (
    Flask, flash, render_template, redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/get_cooking")
def get_cooking():
    cooking = mongo.db.cooking.find()
    return render_template("cooking.html", cooking=cooking)


@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"first_name": request.form.get("first_name").lower(),
             "last_name": request.form.get("last_name").lower()})

        if existing_user:
            flash("Username not free, choose another one")
            return redirect(url_for("registration"))

        registration = {
                "first_name": request.form.get("first_name").lower(),
                "last_name": request.form.get("last_name").lower(),
                "password": generate_password_hash(request.form.get("password")),
                "is_admin": False}
        mongo.db.users.insert_one(registration)


        # put the new user into 'session' cookie
        session["user"] = request.form.get(
                "first_name").lower(), request.form.get("last_name").lower()

        flash("Registration Successfull ")
    return render_template("registration.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)

