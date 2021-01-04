# -*- coding: utf-8 -*-
"""
Requires Python 3.8 or later
"""

__author__ = "Jorge Morfinez Mojica (jorge.morfinez.m@gmail.com)"
__copyright__ = "Copyright 2020, Jorge Morfinez Mojica"
__license__ = ""
__history__ = """ """
__version__ = "1.1.L31.2 ($Rev: 10 $)"

"""Oracle DB backend (db-oracle).

Each one of the CRUD operations should be able to open a database connection if
there isn't already one available (check if there are any issues with this).

Documentation:

"""

from sqlalchemy import create_engine, Column, Integer, String, Numeric
from sqlalchemy.engine.url import URL
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.exc import TimeoutError
from sqlalchemy.exc import InternalError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from db_controller import mvc_exceptions as mvc_exc
from constants.constants import Constants as Const
from logger_controller.logger_control import *
import psycopg2
from datetime import datetime
import json

import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

Base = declarative_base()
logger = configure_db_logger()


# Datos de conecxion a base de datos
def init_connect_db():
    r"""
    Contiene la inicializacion de datos para conectar a base de datos.
    :return: list_data_cnx
    """
    init_cnx_db_data = []

    cfg = get_config_constant_file()

    # TEST:
    db_host = cfg['DB_RDS']['HOST_DB']
    db_username = cfg['DB_RDS']['USER_DB']
    db_password = cfg['DB_RDS']['PASSWORD_DB']
    db_port = cfg['DB_RDS']['PORT_DB']
    db_driver = cfg['DB_RDS']['SQL_DRIVER']
    db_name = cfg['DB_RDS']['DATABASE_NAME']

    data_connection = [db_host, db_username, db_password, db_port, db_name]

    init_cnx_db_data.append(data_connection)

    return data_connection


def session_to_db():
    data_bd_connection = init_connect_db()

    connection = None

    try:

        if data_bd_connection:

            connection = psycopg2.connect(user=data_bd_connection[1],
                                          password=data_bd_connection[2],
                                          host=data_bd_connection[0],
                                          port=data_bd_connection[3],
                                          database=data_bd_connection[4])

        else:
            logger.error('Some data is not established to connect PostgreSQL DB. Please verify it!')

    except (Exception, psycopg2.Error) as error:
        logger.exception('Can not connect to database, verify data connection to %s', data_bd_connection[4],
                         error, exc_info=True)
        raise mvc_exc.ConnectionError(
            '"{}" Can not connect to database, verify data connection to "{}".\nOriginal Exception raised: {}'.format(
                data_bd_connection[0], data_bd_connection[4], error
            )
        )

    return connection


def scrub(input_string):
    """Clean an input string (to prevent SQL injection).

    Parameters
    ----------
    input_string : str

    Returns
    -------
    str
    """
    return "".join(k for k in input_string if k.isalnum())


def create_cursor(conn):
    try:
        cursor = conn.cursor()

    except (Exception, psycopg2.Error) as error:
        logger.exception('Can not create the cursor object, verify database connection', error, exc_info=True)
        raise mvc_exc.ConnectionError(
            'Can not connect to database, verify data connection.\nOriginal Exception raised: {}'.format(
                error
            )
        )

    return cursor


def disconnect_from_db(conn):
    if conn is not None:
        conn.close()


def close_cursor(cursor):
    if cursor is not None:
        cursor.close()


def get_systimestamp_date(session):
    last_updated_date_column = session.execute('SELECT systimestamp from dual').scalar()

    logger.info('Timestamp from DUAL: %s', last_updated_date_column)

    return last_updated_date_column


def get_datenow_from_db(conn):

    cursor = None
    last_updated_date = None
    sql_nowdate = ''

    try:

        sql_nowdate = 'SELECT now()'

        cursor = create_cursor(conn)

        cursor.execute(sql_nowdate)

        result = cursor.fetchall()

        if result is not None:
            last_updated_date = result

        cursor.close()

    except SQLAlchemyError as error:
        conn.rollback()
        logger.exception('An exception occurred while execute transaction: %s', error)
        raise SQLAlchemyError(
            "A SQL Exception {} occurred while transacting with the database.".format(error)
        )
    finally:
        disconnect_from_db(conn)

    return last_updated_date


def exists_data_row(table_name, column_name, column_filter1, value1, column_filter2, value2):
    r"""
    Transaction that validates the existence and searches for a certain record in the database.

    :param table_name: The table name to looking for data van.
    :param column_name: The name of the column to find existence.
    :param column_filter1: The name of the first column filter to looking for data.
    :param value1: The value of the first filter to looking for data.
    :param column_filter2: The name of the next column filter to looking for data.
    :param value2: The value of the next filter to looking for data.
    :return row_data: The data if row exists.
    """

    conn = None
    cursor = None
    row_data = None

    try:
        conn = session_to_db()
        cursor = conn.cursor()

        sql_exists = f"SELECT {column_name} FROM {table_name} " \
                     f"WHERE {column_filter1} = {value1} AND {column_filter2} = '{value2}'"

        cursor.execute(sql_exists)

        row_exists = cursor.fetchall()

        # row_exists = session.execute(sql_exists)

        for r_e in row_exists:

            logger.info('Row Info in Query: %s', str(r_e))

            if r_e is None:
                r_e = None
            else:
                row_data = r_e[column_name]

            # row_exists.close()

            close_cursor(cursor)

    except SQLAlchemyError as error:
        conn.rollback()
        logger.exception('An exception occurred while execute transaction: %s', error)
        raise SQLAlchemyError(
            "A SQL Exception {} occurred while transacting with the database on table {}.".format(error, table_name)
        )
    finally:
        disconnect_from_db(conn)

    return row_data


def validate_transaction(table_name,
                         column_name,
                         column_filter1, value1,
                         column_filter2, value2,
                         column_filter3, value3):
    r"""
    Transaction that validates the existence and searches for a certain record in the database.

    :param table_name: The table name to looking for data van.
    :param column_name: The name of the column to find existence.
    :param column_filter1: The name of the first column filter to looking for data.
    :param value1: The value of the first filter to looking for data.
    :param column_filter2: The name of the next column filter to looking for data.
    :param value2: The value of the next filter to looking for data.
    :param column_filter3: The name of the next column filter to looking for data.
    :param value3: The value of the next filter to looking for data.
    :return row_data: The data if row exists.
    """

    conn = None
    cursor = None
    row_data = None

    try:
        conn = session_to_db()
        cursor = conn.cursor()

        sql_exists = 'SELECT {} FROM {} WHERE {} = {} AND {} = {} AND {} = {}'.format(column_name, table_name,
                                                                                      column_filter1, value1,
                                                                                      column_filter2, "'" + value2 + "'",
                                                                                      column_filter3, "'" + value3 + "'")

        cursor.execute(sql_exists)

        row_exists = cursor.fetchall()

        for r_e in row_exists:

            logger.info('Row Info in Query: %s', str(r_e))

            if r_e is None:
                r_e = None
            else:
                row_data = r_e[column_name]

            close_cursor(cursor)

    except SQLAlchemyError as error:
        conn.rollback()
        logger.exception('An exception occurred while execute transaction: %s', error)
        raise SQLAlchemyError(
            "A SQL Exception {} occurred while transacting with the database on table {}.".format(error, table_name)
        )
    finally:
        disconnect_from_db(conn)

    return row_data


class UrbvanModelDb(Base):

    r"""
    Class to instance the data of a Van on the database.
    Transactions:
     - Insert: Add Van data to the database if not exists.
     - Update: Update Van data on the database if exists.
    """

    cfg = get_config_constant_file()

    __tablename__ = cfg['DB_OBJECTS']['VAN_TABLE']

    uuid_van = Column(cfg['DB_COLUMNS_DATA']['VAN_VEHICLE']['UUID_VAN'], String, primary_key=True)
    plates_van = Column(cfg['DB_COLUMNS_DATA']['VAN_VEHICLE']['PLATES_VAN'], String)
    economic_number_van = Column(cfg['DB_COLUMNS_DATA']['VAN_VEHICLE']['ECONOMIC_NUMBER'], String)
    seats_van = Column(cfg['DB_COLUMNS_DATA']['VAN_VEHICLE']['SEATS_VAN'], Numeric)
    created_at = Column(cfg['DB_COLUMNS_DATA']['VAN_VEHICLE']['CREATED_AT'], String)
    status_van = Column(cfg['DB_COLUMNS_DATA']['VAN_VEHICLE']['STATUS_VAN'], String)

    def manage_van_vehicle_data(self, uuid_van, plates_van, economic_number_van, seats_van, status_van):

        van_data = {}

        # session = self

        if exists_data_row(self.__tablename__,
                           self.uuid_van,
                           self.uuid_van,
                           uuid_van,
                           self.plates_van,
                           plates_van):

            van_data = update_van_data(self.__tablename__,
                                       uuid_van,
                                       plates_van,
                                       economic_number_van,
                                       seats_van,
                                       status_van)
        else:
            van_data = insert_new_van(self.__tablename__,
                                      uuid_van,
                                      plates_van,
                                      economic_number_van,
                                      seats_van,
                                      status_van)

        return van_data


# Add Van data to insert the row on the database
def insert_new_van(table_name, uuid_van, plates_van, economic_number_van, seats_van, status_van):
    r"""
    Transaction to add data of a Van and inserted on database.
    The data that you can insert are:

    :param table_name: The table name to looking for data van.
    :param uuid_van: UUID to identify the Van registered.
    :param plates_van: Plates of a Van.
    :param economic_number_van: Economic number of a Van.
    :param seats_van: Number of seats of the Van.
    :param status_van: Status of the Van
    :return van_data_inserted: Dictionary that contains Van data inserted on db.
    """

    conn = None
    cursor = None
    van_data_inserted = dict()

    try:
        conn = session_to_db()

        cursor = conn.cursor()

        created_at = get_datenow_from_db(conn)

        data_insert = (uuid_van, plates_van, economic_number_van, seats_van, created_at, status_van,)

        sql_van_insert = 'INSERT INTO {} ' \
                         '(uuid_van, ' \
                         'plates_van, ' \
                         'economic_number_van, ' \
                         'seats_van, ' \
                         'created_at, ' \
                         'status_van, ' \
                         'last_update_date) ' \
                         'VALUES (%s, %s, %s, %s, NOW())'.format(table_name)

        cursor.execute(sql_van_insert, data_insert)

        conn.commit()

        logger.info('Vsn Vehicle inserted %s', "{0}, Plate: {1}".format(uuid_van, plates_van))

        close_cursor(cursor)

        row_exists = validate_transaction(table_name,
                                          'uuid_van',
                                          'uuid_van', uuid_van,
                                          'plates_van', plates_van,
                                          'economic_number_van', economic_number_van)

        if str(uuid_van) not in str(row_exists):

            van_data_inserted = {
                "UUID": uuid_van,
                "Plate": plates_van,
                "EconomicNumber": economic_number_van,
                "SeatsNumber": seats_van,
                "Status": status_van,
                "CreationDate": created_at,
                "Message": "Van Inserted Successful",
            }

        else:
            van_data_inserted = {
                "UUID": uuid_van,
                "Plate": plates_van,
                "EconomicNumber": economic_number_van,
                "SeatsNumber": seats_van,
                "Status": status_van,
                "CreationDate": created_at,
                "Message": "Van already Inserted",
            }

    except SQLAlchemyError as error:
        conn.rollback()
        logger.exception('An exception was occurred while execute transaction: %s', error)
        raise SQLAlchemyError(
            "A SQL Exception {} occurred while transacting with the database on table {}.".format(error, table_name)
        )
    finally:
        disconnect_from_db(conn)

    return json.dumps(van_data_inserted)


# Update van data registered
def update_van_data(table_name, uuid_van, plates_van, economic_number_van, seats_van, status_van):
    r"""
    Transaction to update data of a Van registered on database.
    The data that you can update are:

    :param table_name: The table name to looking for data van.
    :param uuid_van: Can not update an UUID of a van, but use it to looking for and update it.
    :param plates_van: Plates of a van to update.
    :param economic_number_van: Economic number of a van to update.
    :param seats_van: Number of seats of a van to update.
    :param status_van: Status of a van to update.
    :return van_data_updated: Dictionary that contains Van data updated on db.
    """

    conn = None
    cursor = None
    van_data_updated = dict()

    try:
        conn = session_to_db()

        cursor = conn.cursor()

        last_update_date = get_datenow_from_db(conn)

        # update row to database
        sql_update_van = "UPDATE {} SET economic_number_van=%s, seats_van=%s, status_van=%s, last_update_date = NOW()" \
                         " WHERE uuid_van=%s AND plates_van=%s".format(table_name)

        cursor.execute(sql_update_van, (economic_number_van, seats_van, status_van, uuid_van, plates_van,))

        conn.commit()

        close_cursor(cursor)

        row_exists = validate_transaction(table_name,
                                          'status_van',
                                          'uuid_van', uuid_van,
                                          'plates_van', plates_van,
                                          'economic_number_van', economic_number_van)

        if str(status_van) in str(row_exists):

            van_data_updated = {
                "UUID": uuid_van,
                "Plate": plates_van,
                "EconomicNumber": economic_number_van,
                "SeatsNumber": seats_van,
                "Status": status_van,
                "LastUpdateDate": last_update_date,
                "Message": "Van Updated Successful",
            }

        else:

            van_data_updated = {
                "UUID": uuid_van,
                "Plate": plates_van,
                "EconomicNumber": economic_number_van,
                "SeatsNumber": seats_van,
                "Status": status_van,
                "LastUpdateDate": last_update_date,
                "Message": "Van not updated",
            }

            logger.error('Can not read the recordset: {}, beacause is not stored on table: {}'.format(status_van,
                                                                                                      table_name))
            raise SQLAlchemyError(
                "Can\'t read data because it\'s not stored in table {}. SQL Exception".format(table_name)
            )

    except SQLAlchemyError as error:
        conn.rollback()
        logger.exception('An exception occurred while execute transaction: %s', error)
        raise SQLAlchemyError(
            "A SQL Exception {} occurred while transacting with the database on table {}.".format(error, table_name)
        )
    finally:
        disconnect_from_db(conn)

    return json.dumps(van_data_updated)


# Delete van registered by uuid and plates
def delete_van_data(table_name, uuid_van, plate_van):
    r"""
    Transaction to delete a Van data registered on database from his uuid and plates.

    :param table_name: The table name to looking for data van.
    :param uuid_van: Id to looking for a Van data to delete.
    :param plate_van: Plates to looking for a Van data to delete.
    :return van_data_delete: Dictionary contains Van data deleted.
    """

    conn = None
    cursor = None
    van_data_deleted = dict()

    try:
        conn = session_to_db()

        cursor = conn.cursor()

        # delete row to database
        sql_delete_van = "DELETE FROM {} WHERE uuid_van=%s AND plates_van=%s".format(table_name)

        cursor.execute(sql_delete_van, (uuid_van, plate_van,))

        conn.commit()

        close_cursor(cursor)

        van_data_deleted = {
            "UUID": uuid_van,
            "Plate": plate_van,
            "Message": "Van Deleted Successful",
        }

        row_exists = exists_data_row(table_name,
                                     'uuid_van',
                                     'uuid_van', uuid_van,
                                     'plates_van', plate_van)

        if str(uuid_van) in str(row_exists):

            van_data_deleted = {
                "UUID": uuid_van,
                "Plate": plate_van,
                "Message": "Van not deleted",
            }

        else:

            logger.error('Can not read the recordset: {}, because is not stored on table: {}'.format(uuid_van,
                                                                                                     table_name))
            raise mvc_exc.ItemNotStored(
                'Can\'t read "{}" because it\'s not stored in table "{}. SQL Exception"'.format(
                    uuid_van, table_name
                )
            )

    except SQLAlchemyError as error:
        conn.rollback()
        logger.exception('An exception occurred while execute transaction: %s', error)
        raise SQLAlchemyError(
            "A SQL Exception {} occurred while transacting with the database on table {}.".format(error, table_name)
        )
    finally:
        disconnect_from_db(conn)

    return json.dumps(van_data_deleted)


# Select all data van by uuid from db
def select_van_by_uuid(table_name, uuid_van):
    r"""
    Get all the Van's data looking for specific status on database.

    :param table_name: The table name to looking for data van.
    :param uuid_van: Id to looking for a Van data.
    :return data_van_by_uuid: Dictionary that contains all the Van's data by specific UUID.
    """

    conn = None
    cursor = None

    van_data_by_id = []
    data_van_all = dict()

    try:

        conn = session_to_db()

        cursor = conn.cursor()

        sql_van_by_id = " SELECT uuid_van, " \
                        "        plates_van, " \
                        "        economic_number_van, " \
                        "        seats_van, " \
                        "        created_at, " \
                        "        status_van, " \
                        "        last_update_date " \
                        " FROM {} " \
                        " WHERE uuid_van = %s".format(table_name)

        cursor.execute(sql_van_by_id, (uuid_van,))

        result = cursor.fetchall()

        if result is not None:
            for van_data in result:
                if van_data is not None:

                    uuid_van = van_data['uuid_van']
                    plates_van = van_data['plates_van']
                    economic_number = van_data['economic_number_van']
                    seats_van = van_data['seats_van']
                    fecha_creacion = datetime.strptime(str(van_data['created_at']), "%Y-%m-%d %H:%M:%S")
                    status_van = van_data['status_van']
                    fecha_actualizacion = datetime.strptime(str(van_data['last_update_date']), "%Y-%m-%d %H:%M:%S")

                    logger.info('Van Registered: %s', 'VanUUId: {}, '
                                                      'VanPlates: {}, '
                                                      'VanEconomicNumber: {}, '
                                                      'VanSeats: {}, '
                                                      'VanStatus: {}, '
                                                      'VanCreatedAt: {} '.format(uuid_van,
                                                                                 plates_van,
                                                                                 economic_number,
                                                                                 seats_van,
                                                                                 status_van,
                                                                                 fecha_creacion))

                    van_data_by_id += [{
                        "VanVehicle": {
                            "UUID": uuid_van,
                            "Plate": plates_van,
                            "EconomicNumber": economic_number,
                            "SeatsNumber": seats_van,
                            "Status": status_van,
                            "CreationDate": fecha_creacion,
                            "LastUpdateDate": fecha_actualizacion,
                        }
                    }]

                else:
                    logger.error('Can not read the recordset: {}, '
                                 'beacause is not stored on table: {}'.format(uuid_van, table_name))
                    raise SQLAlchemyError(
                        "Can\'t read data because it\'s not stored in table {}. SQL Exception".format(table_name)
                    )
        else:
            logger.error('Can not read the recordset, because is not stored: %s', uuid_van)
            raise mvc_exc.ItemNotStored(
                'Can\'t read "{}" because it\'s not stored in table "{}. SQL Exception"'.format(
                    uuid_van, table_name
                )
            )

        close_cursor(cursor)

        data_van_all = json.dumps(van_data_by_id)

    except SQLAlchemyError as error:
        conn.rollback()
        logger.exception('An exception occurred while execute transaction: %s', error)
        raise SQLAlchemyError(
            "A SQL Exception {} occurred while transacting with the database on table {}.".format(error, table_name)
        )
    finally:
        disconnect_from_db(conn)

    return data_van_all


# Select all data van by status from db
def select_van_by_status(table_name, status_van):
    r"""
    Get all the Van's data looking for specific status on database.

    :param table_name: The table name to looking for data van.
    :param status_van: Status to looking for a Van data.
    :return data_van_by_status: Dictionary that contains all the Van's data by specific status.
    """

    conn = None
    cursor = None

    van_data_by_status = []
    data_van_all = dict()

    try:

        conn = session_to_db()

        cursor = conn.cursor()

        sql_van_by_id = " SELECT uuid_van, " \
                        "        plates_van, " \
                        "        economic_number_van, " \
                        "        seats_van, " \
                        "        created_at, " \
                        "        status_van, " \
                        "        last_update_date " \
                        " FROM {} " \
                        " WHERE status_van = %s".format(table_name)

        cursor.execute(sql_van_by_id, (status_van,))

        result = cursor.fetchall()

        if result is not None:
            for van_data in result:
                if van_data is not None:

                    uuid_van = van_data['uuid_van']
                    plates_van = van_data['plates_van']
                    economic_number = van_data['economic_number_van']
                    seats_van = van_data['seats_van']
                    fecha_creacion = datetime.strptime(str(van_data['created_at']), "%Y-%m-%d %H:%M:%S")
                    status_van = van_data['status_van']
                    fecha_actualizacion = datetime.strptime(str(van_data['last_update_date']), "%Y-%m-%d %H:%M:%S")

                    logger.info('Van Registered: %s', 'VanUUId: {}, '
                                                      'VanPlates: {}, '
                                                      'VanEconomicNumber: {}, '
                                                      'VanSeats: {}, '
                                                      'VanStatus: {}, '
                                                      'VanCreatedAt: {} '.format(uuid_van,
                                                                                 plates_van,
                                                                                 economic_number,
                                                                                 seats_van,
                                                                                 status_van,
                                                                                 fecha_creacion))

                    van_data_by_status += [{
                        "VanVehicle": {
                            "UUID": uuid_van,
                            "Plate": plates_van,
                            "EconomicNumber": economic_number,
                            "SeatsNumber": seats_van,
                            "Status": status_van,
                            "CreationDate": fecha_creacion,
                            "LastUpdateDate": fecha_actualizacion,
                        }
                    }]

                else:
                    logger.error('Can not read the recordset: {}, '
                                 'beacause is not stored on table: {}'.format(status_van, table_name))
                    raise SQLAlchemyError(
                        "Can\'t read data because it\'s not stored in table {}. SQL Exception".format(table_name)
                    )
        else:
            logger.error('Can not read the recordset, because is not stored: %s', status_van)
            raise mvc_exc.ItemNotStored(
                'Can\'t read "{}" because it\'s not stored in table "{}. SQL Exception"'.format(
                    status_van, table_name
                )
            )

        close_cursor(cursor)

        data_van_all = json.dumps(van_data_by_status)

    except SQLAlchemyError as error:
        conn.rollback()
        logger.exception('An exception occurred while execute transaction: %s', error)
        raise SQLAlchemyError(
            "A SQL Exception {} occurred while transacting with the database on table {}.".format(error, table_name)
        )
    finally:
        disconnect_from_db(conn)

    return data_van_all


class UsersAuth(Base):
    r"""
    Class to instance User data to authenticate the API.
    Transactions:
     - Insert: Add user data to the database if not exists.
     - Update: Update user data on the database if exists.
    """

    cfg = get_config_constant_file()

    __tablename__ = cfg['DB_AUTH_OBJECT']['USERS_AUTH']

    user_id = Column(cfg['DB_AUTH_COLUMNS_DATA']['USERS_ORDERS']['USER_ID'], Numeric, primary_key=True)
    user_name = Column(cfg['DB_AUTH_COLUMNS_DATA']['USERS_ORDERS']['USER_NAME'], String, primary_key=True)
    user_password = Column(cfg['DB_AUTH_COLUMNS_DATA']['USERS_ORDERS']['USER_PASSWORD'], String)
    password_hash = Column(cfg['DB_AUTH_COLUMNS_DATA']['USERS_ORDERS']['PASSWORD_HASH'], String)
    last_update_date = Column(cfg['DB_AUTH_COLUMNS_DATA']['USERS_ORDERS']['LAST_UPDATE_DATE'], String)

    @staticmethod
    def manage_user_authentication(self, user_name, user_password, password_hash):

        user_id = 0

        try:

            user_id += 1

            user_verification = validate_user_exists(user_name)

            # insert validation
            if user_verification[0]:

                # update method
                update_user_password_hashed(user_name, password_hash)

            else:
                # insert

                user_id += 1

                insert_user_authenticated(user_id, user_name, user_password, password_hash)

        except SQLAlchemyError as e:
            logger.exception('An exception was occurred while execute transactions: %s', e)
            raise mvc_exc.ItemNotStored(
                'Can\'t insert user_id: "{}" with user_name: {} because it\'s not stored in "{}"'.format(
                    user_id, user_name, UsersAuth.__tablename__
                )
            )


# Transaction to looking for a user on db to authenticate
def validate_user_exists(user_name):
    r"""
    Looking for a user by name on the database to valid authentication.

    :param user_name: The user name to valid authentication on the API.
    :return result: Boolean to valid if the user name exists to authenticate the API.
    """

    cfg = get_config_constant_file()

    conn = session_to_db()

    cursor = conn.cursor()

    table_name = cfg['DB_AUTH_OBJECT']['USERS_AUTH']

    sql_check = "SELECT EXISTS(SELECT 1 FROM {} WHERE user_name = {} LIMIT 1)".format(table_name, "'" + user_name + "'")

    cursor.execute(sql_check)

    result = cursor.fetchone()

    return result


# Transaction to update user' password  hashed on db to authenticate
def update_user_password_hashed(user_name, password_hash):
    r"""
    Transaction to update password hashed of a user to authenticate on the API correctly.

    :param user_name: The user name to update password hashed.
    :param password_hash: The password hashed to authenticate on the API.
    """

    cfg = get_config_constant_file()

    conn = session_to_db()

    cursor = conn.cursor()

    last_update_date = get_datenow_from_db(conn)

    table_name = cfg['DB_AUTH_OBJECT']['USERS_AUTH']

    # update row to database
    sql_update_user = "UPDATE {} SET password_hash = %s, last_update_date = NOW() WHERE user_name = %s".format(
        table_name
    )

    cursor.execute(sql_update_user, (password_hash, user_name,))

    conn.commit()

    close_cursor(cursor)


def insert_user_authenticated(user_id, user_name, user_password, password_hash):
    r"""
    Transaction to add a user data to authenticate to API, inserted on the db.

    :param user_id: The Id of the user to add on the db.
    :param user_name: The user name of the user to add on the db.
    :param user_password:  The password od the user to add on the db.
    :param password_hash: The password hashed to authenticate on the API.
    """

    cfg = get_config_constant_file()

    conn = session_to_db()

    cursor = conn.cursor()

    last_update_date = get_datenow_from_db(conn)

    table_name = cfg['DB_AUTH_OBJECT']['USERS_AUTH']

    data = (user_id, user_name, user_password, password_hash,)

    sql_user_insert = 'INSERT INTO {} (user_id, user_name, user_password, password_hash) ' \
                      'VALUES (%s, %s, %s, %s)'.format(table_name)

    cursor.execute(sql_user_insert, data)

    conn.commit()

    logger.info('Usuario insertado %s', "{0}, User_Name: {1}".format(user_id, user_name))

    close_cursor(cursor)


# Function not used.
def get_data_user_authentication(session, table_name, user_name):
    user_auth = []

    user_auth_data = {}

    try:
        sql_user_data = " SELECT user_name, user_password, password_hash, last_update_date " \
                        " FROM {} " \
                        " WHERE user_name = {} ".format(table_name, "'" + user_name + "'")

        user_auth_db = session.execute(sql_user_data)

        for user in user_auth_db:
            if user is not None:

                user_name_db = user['username']
                user_password_db = user['password']
                password_hash = user['password_hash']
                last_update_date = datetime.strptime(str(user['last_update_date']), "%Y-%m-%d")

                user_auth += [{
                    "username": user_name_db,
                    "password": user_password_db,
                    "password_hash": password_hash,
                    "date_updated": last_update_date
                }]

            else:
                logger.error('Can not read the recordset, beacause is not stored')
                raise SQLAlchemyError(
                    "Can\'t read data because it\'s not stored in table {}. SQL Exception".format(table_name)
                )

        user_auth_data = json.dumps(user_auth)

        user_auth_db.close()

    except SQLAlchemyError as sql_exec:
        logger.exception(sql_exec)
    finally:
        session.close()

    return user_auth_data


# Define y obtiene el configurador para las constantes del sistema:
def get_config_constant_file():
    """
        Contiene la obtencion del objeto config
        para setear datos de constantes en archivo
        configurador

    :rtype: object
    """

    # PROD
    # _constants_file = "/var/www/html/apiTestOrdersTV/constants/constants.yml"

    # TEST
    _constants_file = "constants/constants.yml"

    cfg = Const.get_constants_file(_constants_file)

    return cfg
