source venv/bin/activate

export FLASK_APP=dispensed.py

dir=$(pwd)

export DATABASE_URL="sqlite:///$dir/app.db"
export SQLALCHEMY_TRACK_MODIFICATIONS=False 

rm app.db.old
mv app.db app.db.old
rm -r migrations
flask db init
flask db migrate
flask db upgrade
