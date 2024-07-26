#!/usr/bin/python3

from app import app, db

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # If create_menu_items is still needed, it should be called here or in the appropriate place.
        # from app.routes import create_menu_items
        # create_menu_items()
    app.run(debug=True)
