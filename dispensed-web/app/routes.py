from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from app import app, login, db, auto
from app.forms import LoginForm, RegistrationForm, NewPatientForm, NewDrugForm, AssignDrugForm
from app.models import Nurse, Patient, DrugPackage, Drug, PatientDrug
from werkzeug.urls import url_parse
import datetime

# Redirect to login if not logged in
@login.unauthorized_handler
def unauthorized_callback():
    return redirect('/login?next=' + request.path)

@app.route('/')
@app.route('/index')
@auto.doc('private')
@login_required
def index():
    """Homepage - Shows patient list to logged in users."""
    patients = Patient.query.all()
    return render_template('index.html', title='Home', patients=patients)

@app.route('/drugs')
@auto.doc('private')
@login_required
def drugs():
    """Shows list of drugs."""
    drugs = Drug.query.all()
    return render_template('drugs.html', title='Drugs', drugs=drugs)

@app.route('/assigndrug', methods=['GET', 'POST'])
@login_required
def assign_drug():
    """Assign drug to a patient"""
    p = request.args.get('patient_id')
    patient = Patient.query.filter_by(patient_id=p).first()
    form = AssignDrugForm()
    form.drug.choices = [(d.drug_id, d.name) for d in Drug.query.all()]
    if form.validate_on_submit():
        d = Drug.query.filter_by(drug_id = form.drug.data).first()
        pd = PatientDrug(qty=int(form.qty.data), time=form.time.data)
        pd.drug = d
        patient.drugs.append(pd)
        db.session.add(patient)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('assigndrug.html', title='Assign Drug', patient=patient, form=form)

@app.route('/patient', methods=['GET', 'POST'])
@auto.doc('private')
@login_required
def patient():
    """Displays details for a single patient of the given id."""
    p = request.args.get('patient_id')
    patient = Patient.query.filter_by(patient_id=p).first()
    dp = DrugPackage.query.filter_by(patient_id=p).first()
    return render_template('patient.html', title='Patient Info', patient=patient, drug_package=dp)

@app.route('/login', methods=['GET', 'POST'])
@auto.doc('public')
def login():
    """Login Page
    Redirects user to previous page after login (if applicable)
    """
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
@auto.doc('public')
def logout():
    """Logs the user out"""
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
@auto.doc('public')
def register():
    """Register a new user.
    TODO: This will eventually be behind an admin interface so that nurses can not self-register.
    """
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
@auto.doc('private')
@login_required
def newpatient():
    """Form to add a new patient to the database."""
    form = NewPatientForm()
    if form.validate_on_submit():
        p = Patient(name=form.name.data, age=int(form.age.data), qr_code=form.qr_code.data)
        db.session.add(p)
        db.session.commit()
        flash('New Patient Registered :' + form.name.data)
        return redirect(url_for('index'))
    return render_template('addpatient.html', title='Add Patient', form=form)

@app.route('/newdrug', methods=['GET', 'POST'])
@auto.doc('private')
@login_required
def newdrug():
    """Form to add a new drug."""
    form = NewDrugForm()
    if form.validate_on_submit():
        d = Drug(
            name = form.name.data,
            side_effects = form.side_effects.data,
            restricted = int(form.restricted.data),
            barcode = form.barcode
        )
        db.session.add(d)
        db.session.commit()
        flash('New Drug Registered :' + form.name.data)
        return redirect(url_for('drugs'))
    return render_template('adddrug.html', title='Add Drug', form=form)

@app.route('/doc')
def documentation():
    return auto.html(groups=['public','private'])

@app.route('/dbread')
@auto.doc('public')
def dbread():
    """Read the database and return the patients data in json format"""
    patients = Patient.query.all()
    patients_list = []
    for patient in patients:
        dp = DrugPackage.query.filter_by(patient_id=patient.patient_id).first()
        drugs = []
        for assoc in patient.drugs:
            drug_time = assoc.time.time();
            time1 = datetime.datetime.now() - datetime.timedelta(minutes=15)
            time2 = datetime.datetime.now() + datetime.timedelta(minutes=15)
            if (time1.time() < drug_time and drug_time < time2.time()): 
                drugs.append({'drug_id': assoc.drug.drug_id, 'qty': assoc.qty, 'time': assoc.time.strftime('%H:%M')})
        if (len(drugs) > 0):
            patients_list.append({'patient_id': patient.patient_id, 'qr_code': patient.qr_code, 'drug_package': dp, 'drugs': drugs})
    e = {'dispensing': patients_list}
    return jsonify(e)
