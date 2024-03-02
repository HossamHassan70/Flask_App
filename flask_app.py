from curses import flash
from bson import ObjectId
from flask import Flask, redirect, render_template, request
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/flask"
mongo = PyMongo(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/users")
def users():
    users = list(mongo.db.Student.find(sort=[("Name", 1)]))
    return render_template("userlist.html", users=users)


@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    if request.method == "GET":
        return render_template("add_user.html")
    if request.method == "POST":
        user_data = {
            "name": request.form["name"],
            "age": int(request.form["age"]),
            "location": request.form["location"],
        }
        mongo.db.Student.insert_one(user_data)
        return redirect("/users")
    else:
        return render_template("add_user.html")


@app.route("/update/<id>", methods=["GET", "POST"])
def update_user(id):
    if request.method == "GET":
        the_user = mongo.db.Student.find_one({"_id": ObjectId(id)})
        return render_template("edit_user.html", user=the_user)

    if request.method == "POST":
        data = {
            "name": request.form["name"],
            "age": int(request.form["age"]),
            "location": request.form["location"],
        }
        mongo.db.Student.update_one({"_id": ObjectId(id)}, {"$set": data})
        flash("User was updated!")
        return redirect("/users")


@app.route('/delete/<id>')
def delete_user(id):
    mongo.db.Student.delete_one({'_id': ObjectId(id)})
    flash('User deleted!')
    return redirect('/users')


@app.errorhandler(404)
def not_found_error(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
