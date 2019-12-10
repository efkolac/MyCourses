import psycopg2 as dbapi2

DSN = {'user': "postgres",
       'password': "1234",
       'host': "127.0.0.1",
       'port': "5432",
       'database': "hebe"
       }

create_statement = '''
CREATE TABLE IF NOT EXISTS Place 
  (ID SERIAL PRIMARY KEY     NOT NULL,
  City varchar(255)    NOT NULL,
  District varchar(255)    NOT NULL
  --Street varchar(255)  ,
  --Neighborhood varchar(255),
  --Apartment INTEGER
  
);

CREATE TABLE IF NOT EXISTS Hospital
  (ID SERIAL PRIMARY KEY     NOT NULL,
  Name varchar(1024) NOT NULL,
  Address INTEGER REFERENCES Place(ID) NOT NULL,
  Rate INTEGER  ,
  Capacity INTEGER    NOT NULL DEFAULT 5, -- Doctor capacity
  Handicapped BOOLEAN DEFAULT TRUE,
  Park BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS Human
  (TC INTEGER PRIMARY KEY     NOT NULL,
  Password varchar(255) NOT NULL,
  Authorize varchar(255) NOT NULL, -- ADMIN, DOCTOR, STAFF, NORMAL
  Name varchar(255)    NOT NULL,
  Surname varchar(255)    NOT NULL,
  Mail varchar(255)    NOT NULL,
  Address INTEGER REFERENCES Place(ID) NOT NULL,
  Age INTEGER,
  Height INTEGER,
  Weight INTEGER
);

CREATE TABLE IF NOT EXISTS Doctor
  (ID SERIAL PRIMARY KEY     NOT NULL,
  Human INTEGER REFERENCES Human(TC) ,
  Workdays varchar(255)    NOT NULL, -- 1:monday .. 7:sunday
  Expertise varchar(255)    NOT NULL,
  Hospital INTEGER REFERENCES Hospital(ID) NOT NULL,
  Rate INTEGER
);



CREATE TABLE IF NOT EXISTS History -- Sickness history
  (ID SERIAL PRIMARY KEY     NOT NULL,
  Date TIMESTAMP NOT NULL,
  Doctor INTEGER REFERENCES Doctor(ID),
  Patient INTEGER REFERENCES Human(TC),
  Sickness varchar(255)    NOT NULL,
  Hospital INTEGER REFERENCES Hospital(ID) NOT NULL
);


CREATE TABLE IF NOT EXISTS Appointment -- Sickness history
  (ID SERIAL PRIMARY KEY     NOT NULL,
  Date TIMESTAMP NOT NULL,
  Doctor INTEGER REFERENCES Doctor(ID),
  Patient INTEGER REFERENCES Human(TC),
  Sickness varchar(255)    NOT NULL,
  Feedback varchar(255)    NOT NULL,
  Hospital INTEGER REFERENCES Hospital(ID) NOT NULL,
  Rate_doctor INTEGER,
  Rate_hospital INTEGER
);

'''

try:
    with dbapi2.connect(**DSN) as connection:
        with connection.cursor() as cursor:
            # Print PostgreSQL Connection properties
            print(connection.get_dsn_parameters(), "\n")

            # Print PostgreSQL version
            cursor.execute("SELECT version();")
            record = cursor.fetchone()

            cursor.execute(create_statement)
            connection.commit()
            print("Table created successfully in PostgreSQL ")

            print("You are connected to - ", record, "\n")

except (Exception, dbapi2.Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    # closing database connection.
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
