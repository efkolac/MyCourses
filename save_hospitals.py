import os

import psycopg2 as dbapi2

DSN = {'user': "postgres",
       'password': "1234",
       'host': "127.0.0.1",
       'port': "5432",
       'database': "hebe2"
       }

main_path = "C:\\Users\\Furkan\\PycharmProjects\\hospitals_for_medcheck\\Hospitals"

iller = os.listdir(main_path)

statements = list()

hospitals_file = open('hospitals.sql', 'w')

try:
    with dbapi2.connect(**DSN) as connection:
        with connection.cursor() as cursor:

            for il in iller:
                il_path = os.path.join(main_path, il)
                ilceler = os.listdir(il_path)
                for ilce in ilceler:
                    ilce_path = os.path.join(il_path, ilce)
                    place_id_statement = "SELECT ID FROM place WHERE (city = '{}' AND district = '{}')".format(il, ilce)
                    cursor.execute(place_id_statement)
                    place_id = cursor.fetchone()[0]  # tuple: (1, )
                    hospitals = os.listdir(ilce_path)
                    for hosp in hospitals:
                        insert_hosp_statement = "INSERT INTO hospital(name, address) VALUES ('{}','{}');".format(hosp, place_id)
                        # cursor.execute(insert_hosp_statement)
                        print(insert_hosp_statement, file=hospitals_file)

except (Exception, dbapi2.Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    # closing database connection.
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
