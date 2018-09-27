from flask import Blueprint, render_template
from biller import AccountList

accounts = Blueprint('accounts', __name__,
                        template_folder='templates')

@accounts.route('/')
def index():
    accounts = AccountList.load()
    return render_template("accounts/index.html", title="Accounts", accounts=accounts)