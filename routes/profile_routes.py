from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from bson import ObjectId
import os
import uuid
from models.user_model import users_collection
from models.wallet_model import wallets_collection
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

profile_bp = Blueprint("profile", __name__, url_prefix="/profile")


@profile_bp.route("/", methods=["GET"])
@login_required
def view_profile():
    user = users_collection.find_one({"_id": ObjectId(current_user.id)})
    wallet = wallets_collection.find_one({"user_id": current_user.id})
    return render_template("profile/profile.html", user=user, wallet=wallet)


@profile_bp.route("/update", methods=["POST"])
@login_required
def update_profile():
    first_name = request.form.get("full_name")
    phone_number = request.form.get("phone_number")
    email = request.form.get("email")

    users_collection.update_one(
        {"_id": ObjectId(current_user.id)},
        {"$set": {
            "full_name": first_name,
            "phone_number": phone_number,
            "email": email
        }}
    )
    flash("Profile updated successfully", "success")
    return redirect(url_for("profile.view_profile"))


@profile_bp.route("/change-password", methods=["POST"])
@login_required
def change_password():
    current_password = request.form.get("current_password")
    new_password = request.form.get("new_password")
    confirm_password = request.form.get("confirm_password")

    user = users_collection.find_one({"_id": ObjectId(current_user.id)})

    if not check_password_hash(user["password"], current_password):
        flash("Current password is incorrect", "danger")
        return redirect(url_for("profile.view_profile"))

    if new_password != confirm_password:
        flash("New passwords do not match", "danger")
        return redirect(url_for("profile.view_profile"))

    hashed_password = generate_password_hash(new_password)
    users_collection.update_one(
        {"_id": ObjectId(current_user.id)},
        {"$set": {"password": hashed_password}}
    )
    flash("Password changed successfully", "success")
    return redirect(url_for("profile.view_profile"))


@profile_bp.route("/upload-picture", methods=["POST"])
@login_required
def upload_picture():
    profile_picture = request.files.get("profile_picture")  # <-- fix this line
    if profile_picture:
        filename = secure_filename(profile_picture.filename)
        unique_filename = str(uuid.uuid4()) + "_" + filename
        filepath = os.path.join("static", "uploads", unique_filename)
        profile_picture.save(filepath)

        users_collection.update_one(
            {"_id": ObjectId(current_user.id)},
            {"$set": {"profile_pic": unique_filename}}  # make sure this key matches your template logic
        )
        flash("Profile picture updated", "success")
    else:
        flash("No picture uploaded", "warning")

    return redirect(url_for("profile.view_profile"))

