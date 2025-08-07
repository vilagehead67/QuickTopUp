from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from routes.services.airtime_service import buy_airtime_service
from routes.services.data_service import buy_data_service  # <-- New import
import requests
import os
import uuid
from models.wallet_model import Wallet
from models.transaction_model import record_transaction
PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")


services_bp = Blueprint("services_routes", __name__)

@services_bp.route("/buy-airtime", methods=["GET", "POST"])
def buy_airtime():
    if request.method == "POST":
        phone = request.form.get("phone")
        amount = request.form.get("amount")
        network = request.form.get("network")

        if not all([phone, amount, network]):
            flash("All fields are required.", "danger")
            return redirect(url_for("services_routes.buy_airtime"))

        result = buy_airtime_service(phone, amount, network)

        if result.get("code") == "000":
            flash("Airtime purchase successful!", "success")
        else:
            flash(f"Purchase failed: {result.get('response_description', 'Insufficient fund')}", "danger")

        return redirect(url_for("services_routes.buy_airtime"))

    return render_template("vtu/buy_airtime.html")

@services_bp.route('/data', methods=["GET", "POST"])
@login_required
def data():
    if request.method == "POST":
        phone = request.form.get("phone")
        plan = request.form.get("plan")
        network = request.form.get("network")

        if not all([phone, plan, network]):
            flash("All fields are required.", "danger")
            return redirect(url_for("services_routes.data"))

        result = buy_data_service(phone, plan, network)

        if result.get("code") == "000":
            flash("Data purchase successful!", "success")
        else:
            flash(f"Purchase failed: {result.get('response_description', 'Insufficient fund')}", "danger")

        return redirect(url_for("services_routes.data"))

    return render_template("vtu/buy_data.html")


@services_bp.route("/utility")
@login_required
def utility():
    return render_template("vtu/utility_categories.html")


@services_bp.route('/')
@login_required
def services_home():
    return render_template('services/home.html')


# routes/services_routes.py

@services_bp.route("/wallet/fund", methods=["GET"])
@login_required
def fund_wallet():
    if "user_id" not in session:
        return redirect(url_for("auth_routes.login"))
    return render_template("wallet/fund_wallet.html")

@services_bp.route("/wallet/initiate-funding", methods=["POST"])
@login_required
def initiate_funding():
    amount = int(request.form["amount"])

    email = current_user.email
    user_id = str(current_user.id)  # Make sure your User model has id and email attributes

    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    callback_url = url_for("services_routes.verify_funding", _external=True)
    data = {
        "email": email,
        "amount": amount * 100,
        "reference": str(uuid.uuid4()),
        "callback_url": callback_url
    }

    response = requests.post("https://api.paystack.co/transaction/initialize", json=data, headers=headers)
    res_data = response.json()

    if res_data.get("status"):
        return redirect(res_data["data"]["authorization_url"])
    else:
        flash("Payment initialization failed. Try again.", "danger")
        return redirect(url_for("services_routes.fund_wallet"))


@services_bp.route("/wallet/verify")
def verify_funding():
    reference = request.args.get("reference")
    headers = {
        "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}"
    }

    verify_url = f"https://api.paystack.co/transaction/verify/{reference}"
    response = requests.get(verify_url, headers=headers)
    res_data = response.json()

    if res_data.get("status") and res_data["data"]["status"] == "success":
        amount = res_data["data"]["amount"] // 100  # convert from kobo to naira
        user_id = session.get("user_id")

        # ✅ Update wallet balance using the Wallet class
        Wallet.update_balance(user_id, amount, operation="credit")

        # ✅ Record transaction
        record_transaction(
            user_id=user_id,
            amount=amount,
            txn_type="FUND",
            status="success",
            reference=reference
        )

        flash(f"Wallet funded with ₦{amount}.", "success")
        return redirect(url_for("dashboard.fund_wallet"))

    else:
        flash("Payment verification failed.", "danger")
        return redirect(url_for("services_routes.fund_wallet"))


