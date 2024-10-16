from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp

class CartForm(FlaskForm):
    cartstore_id = IntegerField('Store ID', validators=[DataRequired()])
    cartcustomer_id = IntegerField('Customer ID', validators=[DataRequired()])
    cartstatus = StringField('Status', validators=[DataRequired(), Length(max=50)])
    cartvat = DecimalField('VAT', validators=[DataRequired()])
    cartdiscount = DecimalField('Discount', validators=[DataRequired()])
    carttotal = DecimalField('Total', validators=[DataRequired()])
    cartcurrenttime = StringField('Current Time', validators=[DataRequired(), Regexp(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')])
    carteditedtime = StringField('Edited Time', validators=[DataRequired(), Regexp(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')])
    cartpurchasedtime = StringField('Purchased Time', validators=[DataRequired(), Regexp(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')])
    cartdeliverytime = StringField('Delivery Time', validators=[DataRequired(), Regexp(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')])
    submit = SubmitField('Submit')
