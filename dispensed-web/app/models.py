from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


def str2int(s, chars):
    """Turn alphabetic string into pseudo-unique integer."""
    i = 0
    for c in reversed(s):
        i *= len(chars)
        i += chars.index(c)
    return i


@login.user_loader
def load_user(id):
    return Nurse.query.get(id)


# Association Tables:
drug_patient = db.Table('drug_patient', db.Model.metadata,
                        db.Column('drug_id', db.Integer,
                                  db.ForeignKey('drug.drug_id')),
                        db.Column('patient_id', db.Integer,
                                  db.ForeignKey('patient.patient_id'))
                        )


drug_identifier = db.Table('drug_identifier', db.Model.metadata,
                           db.Column('drug_id', db.Integer,
                                     db.ForeignKey('drug.drug_id')),
                           db.Column('package_id', db.Integer,
                                     db.ForeignKey('package.package_id'))
                           )


# Patient-Drug Association Class
class PatientDrug(db.Model):
    __tablename__ = 'patient_drug'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'))
    drug_id = db.Column(db.Integer, db.ForeignKey('drug.drug_id'))
    drug = db.relationship("Drug")
    qty = db.Column(db.Integer, index=True)
    time = db.Column(db.DateTime, index=True)
    dispensed = db.Column(db.Integer, index=True)


class Nurse(UserMixin, db.Model):
    __tablename__ = 'nurse'
    nurse_id = db.Column(db.String(32), primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def get_id(self):
        return self.nurse_id

    def __repr__(self):
        return '<User {}>'.format(self.nurse_id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Patient(db.Model):
    __tablename__ = 'patient'
    patient_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    age = db.Column(db.Integer, index=True)
    qr_code = db.Column(db.String(64), index=True)
    drugs = db.relationship('PatientDrug')

    def __repr__(self):
        return '<Patient {}>'.format(self.name)


class Drug(db.Model):
    __tablename__ = 'drug'
    drug_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    side_effects = db.Column(db.String(256))
    restricted = db.Column(db.Integer, index=True)
    barcode = db.Column(db.String(64))


class DrugPackage(db.Model):
    __tablename__ = 'package'
    package_id = db.Column(db.Integer, primary_key=True)
    drugs = db.relationship('Drug', secondary=drug_identifier)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'))
