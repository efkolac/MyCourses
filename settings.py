import os.path
import sys

DSN_efk = {'user': "postgres",  # DSN for Emre Faruk Kolaç
           'password': "",
           'host': "127.0.0.1",
           'port': "5432",
           'database': "hebe2"
           }

DSN_fg = {'user': "postgres",  # DSN for Furkan Güvenç
          'password': "1234",
          'host': "127.0.0.1",
          'port': "5432",
          'database': "hebe2"
          }

#  postgres//user:pw@host:port/database

fg_connection_url = "dbname={} user={} password={} host={} port={}".format(DSN_fg['database'], DSN_fg['user'],
                                                                           DSN_fg['password'], DSN_fg['host'],
                                                                           DSN_fg['port'])

efk_connection_url = "dbname={} user={} password={} host={} port={}".format(DSN_efk['database'], DSN_efk['user'],
                                                                            DSN_efk['password'], DSN_efk['host'],
                                                                            DSN_efk['port'])
HOME_PATH = os.path.expanduser("~").lower()  # home url of pc
db_url = str()

try:
    if 'furkan' in HOME_PATH:  # Pc of Furkan Güvenç
        db_url = fg_connection_url
    elif 'faruk' in HOME_PATH:  # Pc of Emre Faruk Kolaç
        db_url = efk_connection_url
    elif 'app' in HOME_PATH:  # Heroku
        db_url = os.getenv("DATABASE_URL")
except Exception as e:
    print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
    sys.exit(1)

SQL_DIR = "sqls"
