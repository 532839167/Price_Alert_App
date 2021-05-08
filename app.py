import os

from flask import Flask, render_template
from controller.alerts import alert_blueprint
from controller.stores import store_blueprint
from controller.users import user_blueprint

app = Flask(__name__)
app.secret_key = os.urandom(64)

app.register_blueprint(alert_blueprint, url_prefix="/alerts")
app.register_blueprint(store_blueprint, url_prefix="/stores")
app.register_blueprint(user_blueprint, url_prefix="/users")

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
