from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, BooleanField, SubmitField, SelectField, DateTimeField
from wtforms.validators import DataRequired
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange
from app.models import Nurse
import random, string

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    nurse_id = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_nurse_id(self, nurse_id):
        user = Nurse.query.filter_by(nurse_id=nurse_id.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = Nurse.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class NewPatientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=0)])
    qr_code = StringField('QR Code', validators=[DataRequired()])
    submit = SubmitField('Add Patient')

class NewDrugForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    side_effects = StringField('Side Effects')
    restricted = BooleanField('Restricted Drug?')
    barcode = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(64))
    # barcode is currently randomly generated!!!!
    submit = SubmitField('Add Drug')

class AssignDrugForm(FlaskForm):
    drug = SelectField('Drug', choices=["Select Drug"], coerce=int)
    qty = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    time = DateTimeField('Time (HH:MM)', format='%H:%M', validators=[DataRequired()])
    submit = SubmitField('Add')

class AssignDrugPackageForm(FlaskForm):
    drug = SelectField('Drug', choices=["Select Drug"], coerce=int)
    submit = SubmitField('Add')
