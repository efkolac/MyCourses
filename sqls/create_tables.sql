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
  Rate INTEGER DEFAULT 0,
  Capacity INTEGER    NOT NULL DEFAULT 5, -- Doctor capacity
  Handicapped BOOLEAN DEFAULT TRUE,
  Park BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS Human
  (TC CHAR PRIMARY KEY     NOT NULL,
  Password varchar(255) NOT NULL,
  Authorize varchar(255) NOT NULL DEFAULT 'normal', -- ADMIN, DOCTOR, STAFF, NORMAL
  Name varchar(255)    NOT NULL,
  Surname varchar(255)    NOT NULL,
  Mail varchar(255)    NOT NULL,
  Address INTEGER REFERENCES Place(ID) NOT NULL,
  Age INTEGER DEFAULT 0,
  Height INTEGER DEFAULT 0,
  Weight INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS Doctor
  (ID SERIAL PRIMARY KEY     NOT NULL,
  Human CHAR REFERENCES Human(TC) ,
  Workdays varchar(255)    NOT NULL, -- 1:monday .. 7:sunday
  Expertise varchar(255)    NOT NULL,
  Hospital INTEGER REFERENCES Hospital(ID) NOT NULL,
  Rate INTEGER DEFAULT 0
);



CREATE TABLE IF NOT EXISTS History -- Sickness history
  (ID SERIAL PRIMARY KEY     NOT NULL,
  Date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  Doctor INTEGER REFERENCES Doctor(ID),
  Patient CHAR REFERENCES Human(TC),
  Sickness varchar(255)    NOT NULL DEFAULT ' ',
  Hospital INTEGER REFERENCES Hospital(ID) NOT NULL
);


CREATE TABLE IF NOT EXISTS Appointment -- Sickness history
  (ID SERIAL PRIMARY KEY     NOT NULL,
  Date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  Doctor INTEGER REFERENCES Doctor(ID),
  Patient CHAR REFERENCES Human(TC),
  Sickness varchar(255)    NOT NULL DEFAULT ' ',
  Feedback varchar(255)    NOT NULL DEFAULT ' ',
  Hospital INTEGER REFERENCES Hospital(ID) NOT NULL,
  Rate_doctor INTEGER DEFAULT 0,
  Rate_hospital INTEGER DEFAULT 0
);
