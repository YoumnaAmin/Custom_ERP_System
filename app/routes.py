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

@app.route("/home/orders", methods=['GET', 'POST'])
def orders_page():
    form = OrderForm()
    menu_items = Menu.query.all()
    form.order.choices = [(item.name, f"{item.name} - ${item.price}") for item in menu_items]

    if form.validate_on_submit():
        client = Client.query.filter_by(phone=form.phone.data).first()
        if not client:
            client = Client(name=form.customer_name.data, address=form.address.data, phone=form.phone.data)
            db.session.add(client)
            db.session.commit()  # Ensure the client ID is assigned
        else:
            client.name = form.customer_name.data
            client.address = form.address.data
            db.session.commit()  # Commit the updates to the client

        new_order = Order(client_id=client.id, item=form.order.data, quantity=form.quantity.data, date=form.date.data)
        db.session.add(new_order)
        db.session.commit()
        flash('Order has been created!', 'success')
        return redirect(url_for('orders_page'))

    elif request.method == 'GET' and 'phone' in request.args:
        client = Client.query.filter_by(phone=request.args.get('phone')).first()
        if client:
            return {
                "name": client.name,
                "address": client.address
            }
        else:
            return {}

    orders = Order.query.order_by(Order.date.desc()).all()
    return render_template('orders.html', title="Orders", form=form, orders=orders, menu_items=menu_items)


@app.route("/new_order", methods=['GET', 'POST'])
def new_order_page():
    form = OrderForm()
    menu_items = Menu.query.all()
    form.order.choices = [(item.name, f"{item.name} - ${item.price}") for item in menu_items]

    if form.validate_on_submit():
        # Check if the client exists
        client = Client.query.filter_by(phone=form.phone.data).first()
        if not client:
            client = Client(name=form.customer_name.data, address=form.address.data, phone=form.phone.data)
            db.session.add(client)
            db.session.commit()  # Commit the client creation before using its ID
        else:
            client.name = form.customer_name.data
            client.address = form.address.data
            db.session.commit()  # Commit the updates to the client

        # Create the order
        new_order = Order(client_id=client.id, date=form.date.data)
        db.session.add(new_order)
        db.session.commit()

        # Create OrderItems
        item_names = form.order.data
        item_quantities = form.quantity.data
        item_prices = [Menu.query.filter_by(name=name).first().price for name in item_names]

        for name, quantity, price in zip(item_names, item_quantities, item_prices):
            order_item = OrderItem(order_id=new_order.id, item=name, quantity=quantity, price=price)
            db.session.add(order_item)

        db.session.commit()
        flash('Order has been created!', 'success')
        return redirect(url_for('orders_page'))

    # Handle GET request and phone lookup
    elif request.method == 'GET' and 'phone' in request.args:
        client = Client.query.filter_by(phone=request.args.get('phone')).first()
        if client:
            return {
                "name": client.name,
                "address": client.address
            }
        else:
            return {}

    return render_template('new_order.html', title="New Order", form=form)

@app.route("/order/<int:order_id>", methods=['GET', 'POST'])
def order_details(order_id):
    order = Order.query.get_or_404(order_id)
    client = Client.query.get(order.client_id)
    menu_items = Menu.query.all()

    form = OrderForm()
    form.order.choices = [(item.name, f"{item.name} - ${item.price}") for item in menu_items]

    if form.validate_on_submit():
        # Update existing order items
        OrderItem.query.filter_by(order_id=order_id).delete()  # Clear existing items

        item_names = form.order.data
        item_quantities = form.quantity.data
        item_prices = [Menu.query.filter_by(name=name).first().price for name in item_names]

        for name, quantity, price in zip(item_names, item_quantities, item_prices):
            order_item = OrderItem(order_id=order_id, item=name, quantity=quantity, price=price)
            db.session.add(order_item)

        # Handle client phone number uniqueness
        existing_client = Client.query.filter_by(phone=form.phone.data).first()
        if existing_client and existing_client.id != client.id:
            flash('Phone number already exists for another client.', 'danger')
        else:
            client.name = form.customer_name.data
            client.address = form.address.data
            client.phone = form.phone.data
            db.session.commit()

            flash('Order has been updated!', 'success')
            return redirect(url_for('order_details', order_id=order.id))

    elif request.method == 'GET':
        # Pre-fill the form with existing order and client details
        order_items = OrderItem.query.filter_by(order_id=order_id).all()
        form.order.data = [item.item for item in order_items]
        form.quantity.data = [item.quantity for item in order_items]
        form.date.data = order.date
        form.customer_name.data = client.name
        form.address.data = client.address
        form.phone.data = client.phone

    # Combine order items and quantities for template
    order_items_with_quantities = zip(form.order.data, form.quantity.data)

    return render_template('order_details.html', title=f"Order {order.id}", order=order, form=form, client=client, order_items_with_quantities=order_items_with_quantities)

@app.route("/order/<int:order_id>/delete", methods=['POST'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    flash('Order has been deleted!', 'success')
    return redirect(url_for('orders_page'))
  
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
