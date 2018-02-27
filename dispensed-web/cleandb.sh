rm app.db.old
mv app.db app.db.old
rm -r migrations
flask db init
flask db migrate
flask db upgrade
