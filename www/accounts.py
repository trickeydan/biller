from flask import Blueprint, render_template, abort
from biller import AccountList

accounts = Blueprint('accounts', __name__,
                        template_folder='templates')

@accounts.route('/')
def index():
    accounts = AccountList.load()
    return render_template("accounts/index.html", title="Accounts", accounts=accounts)

@accounts.route('/<string:account_slug>')
def view(account_slug):
    accounts = AccountList.load()
    try:
        account = accounts.get_account(account_slug)
        return render_template("accounts/view.html", title=account.name, account=account)
    except KeyError:
        abort(404)