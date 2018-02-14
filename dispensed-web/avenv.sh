source venv/bin/activate

export FLASK_APP=dispensed.py

export SQLALCHEMY_DATABASE_UR=I/afs/inf.ed.ac.uk/user/s15/s1529373/sdp/dispensed-web/app.db
export SQLALCHEMY_TRACK_MODIFICATIONS=False 
flask run

