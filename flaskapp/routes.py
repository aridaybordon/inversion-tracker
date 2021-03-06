import flask

from flaskapp import app

from scripts.database import return_degiro_balance_old

@app.route('/')
def home():
    balance, labels = return_degiro_balance_old(50)
    return flask.render_template('index.jinja2', labels=labels, balance=balance)