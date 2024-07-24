#!/usr/bin/python3

from app import app, db
from app.routes import create_menu_items 

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_menu_items()
    app.run(debug=True)
