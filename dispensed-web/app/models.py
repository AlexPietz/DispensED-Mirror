from app import db

class Nurse(db.Model):
    nurse_id = db.Column(db.String(32), primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.nurse_id)


class Patient(db.Model):
    patient_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    age = db.Column(db.Integer, index=True)

    def __repr__(self):
        return '<Patient {}>'.format(self.name)


class Drug(db.Model):
    drug_id = db.Column(db.Integer, primary_key=True)
    side_effects = db.Column(db.String(256))
    restricted = db.Column(db.Integer, index=True)
    barcode = db.Column(db.String(64))


drug_identifier = db.Table('drug_identifier',
    db.Column('drug_id', db.Integer, db.ForeignKey('drug.drug_id')),
    db.Column('patient_id', db.Integer, db.ForeignKey('patient.patient_id'))
)

class DrugPackage(db.Model):
    package_id = db.Column(db.Integer, primary_key=True)
    drugs = db.relationship('Drug', secondary=drug_identifier)
