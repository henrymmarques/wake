from flask import Blueprint, json, render_template, request, jsonify, redirect, url_for

views = Blueprint(__name__, "wake")

@views.route("/")
def home():
    return render_template("index.html", name="welcome to wake")

@views.route("/profile")
def profile():
    return render_template("profile.html")

@views.route("/json")
def get_json():
    return jsonify({'name': 'tim', 'coolness': 10})

@views.route("/data")
def get_data():
    data = request.json
    return jsonify(data)

@views.route("/go-to-home")
def go_to_home():
    return redirect(url_for("views.home"))

@views.route("/aboutUs")
def about_us():
    return render_template("aboutUs.html")

@views.route("/chart")
def chart():
    return render_template("chart.html")