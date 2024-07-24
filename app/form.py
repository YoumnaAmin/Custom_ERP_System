#!/usr/bin/python3

from flask_wtf import FlaskForm
from wtforms import StringField,FormField, FieldList, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, DateField
from wtforms.validators import DataRequired, length, Email, EqualTo, ValidationError
from app.models import Employee


class Register(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = Employee.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('The Username is taken!')
    def validate_email(self, email):
        user = Employee.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('The Email already exists!')
class login(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('login')

class OrderItemForm(FlaskForm):
    item = SelectField('Item', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])

class OrderForm(FlaskForm):
    customer_name = StringField('Customer Name', validators=[DataRequired()])
    address = StringField('Address')
    phone = StringField('Phone', validators=[DataRequired()])
    order = SelectField('Order', choices=[], validators=[DataRequired()])  # Choices will be populated dynamically
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    items = FieldList(FormField(OrderItemForm), min_entries=1, max_entries=10)
    submit = SubmitField('Submit Order')
