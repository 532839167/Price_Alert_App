import json
from flask import Blueprint, render_template, request, redirect, url_for, session
from model.alert import Alert
from model.store import Store
from model.item import Item
from model.user import login_required

alert_blueprint = Blueprint('alerts', __name__)


@alert_blueprint.route('/')
@login_required
def index():
    alerts = Alert.find_many_by("user_email", session["email"])
    return render_template('alerts/index.html', alerts=alerts)


@alert_blueprint.route('/new', methods=['GET', 'POST'])
@login_required
def create_alert():
    if request.method == 'POST':
        item_url = request.form['item_url']

        store = Store.find_by_url(item_url)
        item = Item(item_url, store.tag_name, store.query)
        item.load_price()
        item.save_to_mongo()

        alert_name = request.form['name']
        price_limit = request.form['price_limit']

        Alert(alert_name, item._id, price_limit, session["email"]).save_to_mongo()

    # What happens if it's a GET request
    return render_template("alerts/new_alert.html")


@alert_blueprint.route('/edit/<string:alert_id>', methods=['GET', 'POST'])
@login_required
def edit_alert(alert_id):
    if request.method == 'POST':
        price_limit = float(request.form['price_limit'])

        alert = Alert.get_by_id(alert_id)
        alert.price_limit = price_limit
        alert.save_to_mongo()

        return redirect(url_for('.index'))

    return render_template("alerts/edit_alert.html", alert=Alert.get_by_id(alert_id))


@alert_blueprint.route('/delete/<string:alert_id>')
@login_required
def delete_alert(alert_id):
    alert = Alert.get_by_id(alert_id)
    if alert.user_email == session["email"]:
        alert.remove_from_mongo()
    return redirect(url_for('.index'))
