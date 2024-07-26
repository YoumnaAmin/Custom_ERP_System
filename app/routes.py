#!/usr/bin/python3

from app.models import Employee, Order, Client, Menu, OrderItem
from app.form import Register, login, OrderForm
from app import app, db, bcrypt  # Import db and bcrypt from your app's __init__.py
from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app
from flask_login import login_user, current_user, logout_user

orders_bp = Blueprint('orders', __name__)

@app.route("/", methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = login()
    if form.validate_on_submit():
        user = Employee.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home_page'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = Register()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Employee(username=form.username.data, email=form.email.data, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}, you can login now!', 'success')
        return redirect(url_for('login_page'))
    return render_template('register.html', title="Register", form=form)

@app.route("/home")
def home_page():
    return render_template('home.html', title="Home")

# Create some dummy data for the menu
def create_menu_items():
        if Menu.query.count() == 0:
            items = [
                {"name": "Box of Chocolate", "price": 2.0},
                {"name": "Pack of Biscuits", "price": 1.5},
                {"name": "Bag of Chips", "price": 1.0}
            ]
            for item in items:
                menu_item = Menu(name=item["name"], price=item["price"])
                db.session.add(menu_item)
            db.session.commit()
@orders_bp.route('/new_order', methods=['GET', 'POST'])
def new_order_page():
    # Your view function here
    pass

@orders_bp.route('/order/<int:order_id>', methods=['GET', 'POST'])
def order_details(order_id):
    # Your view function here
    pass

@orders_bp.route('/delete_order/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    # Your view function here
    pass

@app.route("/customers")
def customers_page():
    return render_template('customers.html', title="Customers")

@app.route("/menu")
def menu_page():
    return render_template('menu.html', title="Menu")

@app.route("/inventory")
def inventory_page():
    return render_template('inventory.html', title="Inventory")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home_page'))
