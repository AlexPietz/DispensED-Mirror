from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, login, db
from app.forms import LoginForm, RegistrationForm, NewPatientForm
from app.models import Nurse, Patient, DrugPackage
from werkzeug.urls import url_parse

# Redirect to login if not logged in
@login.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?next=' + request.path)

@app.route('/')
@app.route('/index')
@login_required
def index():
    patients = Patient.query.all()
    return render_template('index.html', title='Home', patients=patients)

@app.route('/patient', methods=['GET', 'POST'])
@login_required
def patient():
    p = request.args.get('patient_id')
    patient = Patient.query.filter_by(patient_id=p).first()
    dp = DrugPackage.query.filter_by(patient_id=p).first()
    return render_template('patient.html', title='Patient Info', patient=patient, drug_package=dp)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Nurse.query.filter_by(nurse_id=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Nurse(nurse_id=form.nurse_id.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/newpatient', methods=['GET', 'POST'])
@login_required
def newpatient():
    form = NewPatientForm()
    if form.validate_on_submit():
        p = Patient(name=form.name.data, age=int(form.age.data))
        db.session.add(p)
        db.session.commit()
        flash('New Patient Registered ' + form.name.data)
        return redirect(url_for('index'))
    return render_template('addpatient.html', title='Add Patient', form=form)