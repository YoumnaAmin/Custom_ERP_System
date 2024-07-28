from flask import Blueprint, render_template, redirect, url_for, flash
from app.models import Menu, db
from app.form import MenuItemForm

menu_bp = Blueprint('menu_bp', __name__)

@menu_bp.route("/menu", methods=['GET', 'POST'])
def menu_page():
    form = MenuItemForm()
    if form.validate_on_submit():
        new_item = Menu(name=form.name.data, price=form.price.data)
        db.session.add(new_item)
        db.session.commit()
        flash('Menu item has been added!', 'success')
        return redirect(url_for('menu_bp.menu_page'))

    menu_items = Menu.query.all()
    return render_template('menu.html', form=form, menu_items=menu_items)

@menu_bp.route("/menu/edit/<int:item_id>", methods=['GET', 'POST'])
def edit_menu_item(item_id):
    item = Menu.query.get_or_404(item_id)
    form = MenuItemForm(obj=item)
    if form.validate_on_submit():
        item.name = form.name.data
        item.price = form.price.data
        db.session.commit()
        flash('Menu item has been updated!', 'success')
        return redirect(url_for('menu_bp.menu_page'))
    return render_template('edit_menu_item.html', form=form, item=item)

@menu_bp.route("/menu/delete/<int:item_id>", methods=['POST'])
def delete_menu_item(item_id):
    item = Menu.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Menu item has been deleted!', 'success')
    return redirect(url_for('menu_bp.menu_page'))
