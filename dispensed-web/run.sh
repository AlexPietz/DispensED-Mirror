source venv/bin/activate

export FLASK_APP=dispensed.py

dir=$(pwd)

export DATABASE_URL="sqlite:///$dir/app.db"
export SQLALCHEMY_TRACK_MODIFICATIONS=False 

while [ "$1" != "" ]; do
    PARAM=`echo $1 | awk -F= '{print $1}'`
    case $PARAM in
        -d)
            export FLASK_DEBUG=1
            ;;
        --demo)
            export FLASK_DEBUG=1
            export DEMO="True"
            export DATABASE_URL="sqlite:///$dir/demo.db"
            echo "Starting SMTP server on port 2525"
            python -m smtpd -n -c DebuggingServer localhost:2525 &
            ;;
        --demo-init)
            export DEMO="True"
            export  DATABASE_URL="sqlite:///$dir/demo.db"
            echo "Setting up database.."
            mv migrations migrations_temp
            echo "DB INIT:"
            flask db init
            echo "DB MIGRATE:"
            flask db migrate
            echo "DB UPGRADE:"
            flask db upgrade
            exit 1
            ;;
        *)
            echo "Unknown Parameter $PARAM"
            ;;
    esac
    shift
done


flask run --host=0.0.0.0

echo "Shut down web server!"
echo "Shutting down SMTP server.."
kill $!
echo "Finished."



