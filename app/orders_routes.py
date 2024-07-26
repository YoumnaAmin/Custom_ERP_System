# orders_routes.py

from app.models import Order, Client, Menu, OrderItem
from app.form import OrderForm
from app import db
from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app


orders_bp = Blueprint('orders_bp', __name__)

@orders_bp.route("/home/orders", methods=['GET', 'POST'])
def orders_page():
    form = OrderForm()
    menu_items = Menu.query.all()
    item_choices = [(item.name, f"{item.name} - ${item.price}") for item in menu_items]

    # Populate choices for each item in the FieldList
    for item_form in form.items:
        item_form.item.choices = item_choices

    if form.validate_on_submit():
        client = Client.query.filter_by(phone=form.phone.data).first()
        if not client:
            client = Client(name=form.customer_name.data, address=form.address.data, phone=form.phone.data)
            db.session.add(client)
            db.session.commit()
        else:
            client.name = form.customer_name.data
            client.address = form.address.data
            db.session.commit()

        new_order = Order(client_id=client.id, date=form.date.data)
        db.session.add(new_order)
        db.session.commit()

        for item_form in form.items:
            order_item = OrderItem(
                order_id=new_order.id,
                item=item_form.item.data,
                quantity=item_form.quantity.data,
                price=Menu.query.filter_by(name=item_form.item.data).first().price
            )
            db.session.add(order_item)

        db.session.commit()
        flash('Order has been created!', 'success')
        return redirect(url_for('orders_bp.orders_page'))

    elif request.method == 'GET' and 'phone' in request.args:
        client = Client.query.filter_by(phone=request.args.get('phone')).first()
        if client:
            return {"name": client.name, "address": client.address}
        else:
            return {}

    orders = Order.query.order_by(Order.date.desc()).all()
    return render_template('orders.html', title="Orders", form=form, orders=orders, menu_items=menu_items)

@orders_bp.route("/new_order", methods=['GET', 'POST'])
def new_order_page():
    form = OrderForm()
    menu_items = Menu.query.all()
    item_choices = [(item.name, f"{item.name} - ${item.price}") for item in menu_items]

    for item_form in form.items:
        item_form.item.choices = item_choices

    if form.validate_on_submit():
        # Check if the client exists
        client = Client.query.filter_by(phone=form.phone.data).first()
        if not client:
            client = Client(name=form.customer_name.data, address=form.address.data, phone=form.phone.data)
            db.session.add(client)
            db.session.commit()
        else:
            client.name = form.customer_name.data
            client.address = form.address.data
            db.session.commit()

        # Create the order
        new_order = Order(client_id=client.id, date=form.date.data)
        db.session.add(new_order)
        db.session.commit()

        # Create OrderItems
        for item_form in form.items:
            order_item = OrderItem(
                order_id=new_order.id,
                item=item_form.item.data,
                quantity=item_form.quantity.data,
                price=Menu.query.filter_by(name=item_form.item.data).first().price
            )
            db.session.add(order_item)

        db.session.commit()
        flash('Order has been created!', 'success')
        return redirect(url_for('orders_bp.orders_page'))

    elif request.method == 'GET' and 'phone' in request.args:
        client = Client.query.filter_by(phone=request.args.get('phone')).first()
        if client:
            return {"name": client.name, "address": client.address}
        else:
            return {}

    return render_template('new_order.html', title="New Order", form=form)

@orders_bp.route("/order/<int:order_id>", methods=['GET', 'POST'])
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
            return redirect(url_for('orders_bp.order_details', order_id=order.id))

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

@orders_bp.route("/order/<int:order_id>/delete", methods=['POST'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    flash('Order has been deleted!', 'success')
    return redirect(url_for('orders_bp.orders_page'))
