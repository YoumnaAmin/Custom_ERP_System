#!/usr/bin/python3

from app.models import Employee, Order, Client, Menu, OrderItem
from app.form import Register, login, OrderForm
from app import app, db, bcrypt  # Import db and bcrypt from your app's __init__.py
from flask import render_template, url_for, flash, redirect, request, current_app
from flask_login import login_user, current_user, logout_user


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

@app.route("/customers")
def customers_page():
    return render_template('customers.html', title="Customers")

@app.route("/inventory")
def inventory_page():
    return render_template('inventory.html', title="Inventory")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home_page'))
