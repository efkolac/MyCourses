import psycopg2 as dbapi2
import sys
from settings import db_url


def get_address_id(cursor, city: str, district: str) -> int:
    """
    It returns addres id from place table according to city and district
    
    :param cursor: Connection cursor
    :param city: City
    :param district: District
    :return: Address id of district of city
    """
    address_statement = "SELECT ID FROM place WHERE (city = '{}' AND district = '{}');".format(city,
                                                                                               district)
    cursor.execute(address_statement)
    address_id = cursor.fetchone()[0]
    return address_id


def get_hospitals(limit: int = 100, city: str = None, district: str = None) -> list:
    """

    :param limit:
    :param city:
    :param district:
    :return:
    """

    try:
        with dbapi2.connect(db_url) as connection:
            with connection.cursor() as cursor:
                statement = "SELECT hospital.name, place.city, place.district, hospital.rate, hospital.handicapped, hospital.park " \
                            "FROM hospital, place "
                if city:
                    if district:  # city and district
                        statement += "WHERE hospital.address = place.id AND place.city = '{}' " \
                                     "AND place.district = '{}' ".format(city, district)
                    else:  # just city
                        statement += "WHERE hospital.address = place.id AND place.city = '{}' ".format(city)

                elif district:  # just district
                    statement += "WHERE hospital.address = place.id AND place.district = '{}' ".format(district)
                else:  # fetch all hospitals
                    statement += "WHERE hospital.address = place.id "

                statement += "ORDER BY name LIMIT {}".format(limit)

                cursor.execute(statement)
                record = cursor.fetchall()
                return record

    except (Exception, dbapi2.Error) as error:
        print("Error while connecting to PostgreSQL: {}".format(error), file=sys.stderr)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()


def add_hospital(name: str = None, city: str = None, district: str = None, park: bool = False,
                 handicapped: bool = True) -> str:
    try:
        with dbapi2.connect(db_url) as connection:
            with connection.cursor() as cursor:

                address = get_address_id(cursor, city, district)

                add_statement = "INSERT INTO hospital(name, address,park,handicapped) " \
                                "VALUES('{}',{},'{}','{}');".format(name, address, park, handicapped)

                cursor.execute(add_statement)
                print("hebe")
                return "Succesfull"

    except (Exception, dbapi2.Error) as error:
        print("Error while connecting to PostgreSQL: {}".format(error), file=sys.stderr)
        return str(error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()


def add_human(tc, password, authorize, name, surname, mail, address) -> str:
    try:
        with dbapi2.connect(db_url) as connection:
            with connection.cursor() as cursor:
                print(tc, password, authorize, name, surname, mail, address)
                statement = "insert into human " \
                            "values ('{}','{}','{}','{}','{}','{}','{}');".format(tc, password, authorize, name,
                                                                                  surname, mail, address)
                cursor.execute(statement)
                return "successful"

    except (Exception, dbapi2.Error) as error:
        return "Error"
    finally:
        if connection:
            cursor.close()
            connection.close()


def delete_doctor(doctor_tc) -> str:
    try:
        with dbapi2.connect(db_url) as connection:
            with connection.cursor() as cursor:
                statement = "delete from doctor where id = '{}';".format(doctor_tc)
                cursor.execute(statement)
                return "successful"
    finally:
        if connection:
            cursor.close()
            connection.close()


def add_doctor(human_id, workdays, expertise, hospital_id):
    try:
        with dbapi2.connect(db_url) as connection:
            with connection.cursor() as cursor:
                print("yeni doktordayız")
                statement = "insert into doctor(human, workdays, expertise, hospital)"\
                "values('{}','{}','{}','{}');".format(human_id, workdays, expertise, hospital_id)
                cursor.execute(statement)
                return "successful"

    finally:
        if connection:
            cursor.close()
            connection.close()


def log_in(tc, password):
    try:
        with dbapi2.connect(db_url) as connection:
            with connection.cursor() as cursor:
                statement = "select password from human where(tc='{}');".format(tc)
                a = cursor.execute(statement)
                print("a:",a)

    finally:
        if connection:
            cursor.close()
            connection.close()

