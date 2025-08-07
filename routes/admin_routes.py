# routes/admin_routes.py
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.wallet_model import Wallet
from models.transaction_model import transactions_collection
from models.user_model import users_collection
from utils.decorators import admin_required

admin_bp = Blueprint('admin', __name__, url_prefix="/admin")


@admin_bp.route("/dashboard")
@login_required
@admin_required
def dashboard():
    # Get total number of users
    total_users = users_collection.count_documents({})

    # Get total number of transactions
    total_transactions = transactions_collection.count_documents({})

    # Sum all wallet balances
    wallets = Wallet.get_all_wallets()
    total_wallet_balance = sum(wallet.get("balance", 0) for wallet in wallets)

    return render_template("admin/dashboard.html",
                           total_users=total_users,
                           total_transactions=total_transactions,
                           total_wallet_balance=total_wallet_balance)
