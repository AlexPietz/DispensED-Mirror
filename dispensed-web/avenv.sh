source venv/bin/activate

export FLASK_APP=dispensed.py

dir=$(pwd)

export SQLALCHEMY_DATABASE_URI="$dir/app.db"
export SQLALCHEMY_TRACK_MODIFICATIONS=False 

while [ "$1" != "" ]; do
    PARAM=`echo $1 | awk -F= '{print $1}'`
    case $PARAM in
        -d)
            export FLASK_DEBUG=1
            ;;
        *)
            echo "Unknown Parameter $PARAM"
            ;;
    esac
    shift
done

flask run

echo "Finished."



