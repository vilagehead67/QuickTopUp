from flask import Blueprint, render_template
from flask_login import login_required, current_user
from database import users_collection, transactions_collection
from bson import ObjectId

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')



@dashboard_bp.route('/')
@login_required
def dashboard():
    user_id = current_user.get_id()
    
    user = users_collection.find_one({"_id": ObjectId(user_id)})

    transactions = transactions_collection.find({"user_id": user_id}).sort("date", -1).limit(10)

    return render_template('dashboard/dashboard.html', user=user, transactions=transactions)



@dashboard_bp.route('/fund-wallet')
@login_required
def fund_wallet():
    return render_template('wallet/fund_wallet.html')

