from flask import Blueprint, render_template
from flask import request, flash, redirect, url_for, current_app
from flask_mail import Message
from extensions import mail

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

    # Your admin email (recipient)
    admin_email = current_app.config["MAIL_USERNAME"]

    # Compose the email
    msg = Message(
        subject=f"User Message: {subject}",
        sender=email,                  # user is the sender
        recipients=[admin_email],      # admin is the recipient
        body=f"""
        You received a message from the QuickTopUp contact form:

        From: {email}
        Subject: {subject}

        Message:
        {message}
        """
    )

    try:
        mail.send(msg)
        flash("Your message has been sent successfully. We'll get back to you shortly.", "success")
    except Exception as e:
        print(f"[Email Send Error] {e}")
        flash("An error occurred while sending your message. Please try again later.", "danger")

    return redirect(url_for("home.contact"))
