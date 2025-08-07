from flask import Blueprint, render_template

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def homepage():
    return render_template('home.html')  # You need to create this template


@home_bp.route('/about')
def about():
    return render_template('about.html')

from flask import render_template, request, flash, redirect, url_for


@home_bp.route("/contact")
def contact():
    return render_template("contact.html")

@home_bp.route("/contact/submit", methods=["POST"])
def submit_complaint():
    email = request.form["email"]
    subject = request.form["subject"]
    message = request.form["message"]
    
    # You can store this in DB or send email
    print(f"Complaint from {email}: [{subject}] - {message}")
    
    flash("Your message has been received. We'll get back to you shortly.", "success")
    return redirect(url_for("home.contact"))
