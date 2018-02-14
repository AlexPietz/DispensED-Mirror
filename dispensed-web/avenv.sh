source venv/bin/activate
export FLASK_APP=dispensed.py
mydatadir=/tmp/dispensed/db/
mysockfile=/tmp/dispensed/mysql.sock
mypidfile=/tmp/dispensed/mysql.pid

mkdir -p ${mydatadir}
mysql_install_db --datadir=${mydatadir}

/usr/libexec/mysqld --skip-networking \
  --datadir=${mydatadir} \
  --socket=${mysockfile} \
  --pid-file=${mypidfile} &> /dev/null &

nohup mysqladmin --socket=${mysockfile} -u root password 'canttouchthis' 
disown

flask run

mysqladmin --socket=${mysockfile} -u root shutdown
