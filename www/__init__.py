from flask import Flask
from www.config import config
from www.accounts import accounts

app = Flask(__name__)

app.config.update(config)

if 'VIEW_CONFIG' in app.config:
    app.jinja_env.globals['VIEW_CONFIG'] = app.config['VIEW_CONFIG']  # Allow view config access in templates
else:
    app.jinja_env.globals['VIEW_CONFIG'] = {}

app.register_blueprint(accounts, url_prefix='/accounts')

from www import views