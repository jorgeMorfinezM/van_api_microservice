# -*- coding: utf-8 -*-
"""
Requires Python 3.0 or later
"""

__author__ = "Jorge Morfinez Mojica (jorge.morfinez.m@gmail.com)"
__copyright__ = "Copyright 2020, Jorge Morfinez Mojica"
__license__ = ""
__history__ = """ """
__version__ = "1.1.L31.2 ($Rev: 5 $)"

import json
import re
import threading
import time
import uuid

from flask import Flask, jsonify, render_template, json, request
from flask_jwt_extended import JWTManager
from passlib.hash import pbkdf2_sha256 as sha256

from auth_controller.api_authentication import *
from constants.constants import Constants as Const
from logger_controller.logger_control import *
from db_controller.database_backend import *
from model.VanModel import VanModel


logger = configure_ws_logger()


app = Flask(__name__, static_url_path='/static')

app.config['JWT_SECRET_KEY'] = 'ap1_v3h1cl3_urv4n_m1cr0_t3st'
app.config['JWT_BLACKLIST_ENABLED'] = False
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['JWT_ERROR_MESSAGE_KEY'] = 'message'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600
app.config['PROPAGATE_EXCEPTIONS'] = True

jwt = JWTManager(app)


# Se inicializa la App con un hilo para evitar problemas de ejecución
# (Falta validacion para cuando ya exista hilo corriendo)
@app.before_first_request
def activate_job():
    def run_job():
        while True:
            time.sleep(2)

    thread = threading.Thread(target=run_job)
    thread.start()


# Contiene la llamada al HTML que soporta la documentacion de la API,
# sus metodos, y endpoints con los modelos de datos I/O
@app.route('/')
def main():

    return render_template('api_tv_orders.html')


def get_van_by_status(status_van):

    van_list = []

    cfg = get_config_constant_file()

    table_name = cfg['DB_OBJECTS']['VAN_TABLE']

    van_status_list = select_van_by_status(table_name, status_van)

    van_list = json.loads(van_status_list)

    if van_list:

        logger.info('Van list by Status: {}: {}: '.format(status_van, van_list))

        return van_list


@app.route('/api/urbvan/vehicle/van/status/',  methods=['GET', 'OPTIONS'])
@jwt_required
def endpoint_list_van_by_status():

    headers = request.headers
    auth = headers.get('Authorization')

    if not auth and 'Bearer' not in auth:
        return request_unauthorized()
    else:
        if request.method == 'OPTIONS':
            headers = {
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
                'Access-Control-Max-Age': 1000,
                'Access-Control-Allow-Headers': 'origin, x-csrftoken, content-type, accept',
            }
            return '', 200, headers

        elif request.method == 'GET':

            data = request.get_json(force=True)

            status_van = data['status']

            json_data = []

            json_data = get_van_by_status(status_van)

            if not status_van:
                return request_conflict()

            return json.dumps(json_data)

        else:
            return not_found()


def get_van_by_uuid(uuid_van):

    van_list = []

    cfg = get_config_constant_file()

    table_name = cfg['DB_OBJECTS']['VAN_TABLE']

    van_uuid_list = select_van_by_uuid(table_name, uuid_van)

    van_list = json.loads(van_uuid_list)

    if van_list:

        logger.info('Van list by UUID: {}: {}: '.format(uuid_van, van_list))

        return van_list


def update_van_data(uuid_van, plates_van, economic_number_van, seats_van, status_van):
    van_updated = dict()

    cfg = get_config_constant_file()

    table_name = cfg['DB_OBJECTS']['VAN_TABLE']

    van_updated = update_van_data(table_name, uuid_van, plates_van, economic_number_van, seats_van, status_van)

    return van_updated


def delete_van_vehicle(uuid_van, plate_van):

    van_delete_msg = []

    cfg = get_config_constant_file()

    table_name = cfg['DB_OBJECTS']['VAN_TABLE']

    van_delete_response = delete_van_data(table_name, uuid_van, plate_van)

    van_delete_msg = json.loads(van_delete_response)

    if len(van_delete_msg) != 0:
        logger.info('Van deleted: %s', str(van_delete_msg))

        return van_delete_msg


def get_economic_number_van(economic_number_part):
    conn = None
    economic_number_van = None

    try:

        conn = session_to_db()

        economic_number_consecutive = get_nextval_economic_number_van(conn)

        economic_number_van = economic_number_part + '-' + economic_number_consecutive

        regex_eco_num = r"^(\w{2})-(\d{4})$"

        math_part_eco_num = re.match(regex_eco_num, economic_number_van, re.M | re.I)

        if math_part_eco_num:
            return economic_number_van

    except SQLAlchemyError as error:
        raise mvc_exc.ConnectionError(
            'Can\'t connect to database, verify data connection.\nOriginal Exception raised: {}'.format(error)
        )
    finally:
        disconnect_from_db(conn)


def manage_van_requested_data(data_van):

    van_data_response = []

    urbvan_obj = UrbvanModelDb()

    try:

        economic_number_van = str()

        # uuid_van = data_van['uuid_van']
        plates_van = data_van['plate_van']
        economic_number_part_van = data_van['economic_number']
        seats_van = data_van['seats_number']
        status_van = data_van['status']

        regex_part_eco_num = r"^(\w{2})"

        math_part_eco_num = re.match(regex_part_eco_num, economic_number_part_van, re.M | re.I)

        if math_part_eco_num:

            economic_number_van = get_economic_number_van(economic_number_part_van)

            van_obj = VanModel(plates_van, economic_number_van, seats_van, status_van)

            if van_obj.validate_status_apply(status_van):

                uuid_van = van_obj.get_uuid_van()

                response_order = urbvan_obj.manage_van_vehicle_data(uuid_van,
                                                                    plates_van,
                                                                    economic_number_van,
                                                                    seats_van,
                                                                    status_van)

                van_data_response = json.loads(response_order)

                if len(van_data_response) != 0:
                    logger.info('Response Van Data: %s', str(van_data_response))

                    return van_data_response

    except SQLAlchemyError as error:
        raise mvc_exc.ConnectionError(
            'Can\'t connect to database, verify data connection to "{}".\nOriginal Exception raised: {}'.format(
                urbvan_obj.__tablename__, error
            )
        )


@app.route('/api/urbvan/vehicle/van/', methods=['POST', 'GET', 'PUT', 'DELETE', 'OPTIONS'])
@jwt_required
def endpoint_processing_van_data():

    headers = request.headers
    auth = headers.get('Authorization')

    if not auth and 'Bearer' not in auth:
        return request_unauthorized()
    else:
        if request.method == 'OPTIONS':
            headers = {
                'Access-Control-Allow-Methods': 'POST, GET, PUT, DELETE, OPTIONS',
                'Access-Control-Max-Age': 1000,
                'Access-Control-Allow-Headers': 'origin, x-csrftoken, content-type, accept',
            }
            return '', 200, headers

        elif request.method == 'POST':

            data = request.get_json(force=True)

            if not data or str(data) is None:
                return request_conflict()

            logger.info('Data Json Integrador to Manage on DB: %s', str(data))

            json_van_response = manage_van_requested_data(data)

            return json.dumps(json_van_response)

        elif request.method == 'GET':
            data = request.get_json(force=True)

            uuid_van = data['uuid_van']

            logger.info('List Van by UUID: %s', 'UUID_Van: {}'.format(uuid_van))

            json_data = []

            if not uuid_van:
                return request_conflict()

            json_data = get_van_by_uuid(uuid_van)

            logger.info('Van by UUID Info: %s', json_data)

            return json.dumps(json_data)

        elif request.method == 'PUT':

            data_van = request.get_json(force=True)

            if not data_van:
                return request_conflict()

            status_valid = False
            economic_van_number = None

            uuid_van = data_van['uuid_van']
            plates_van = data_van['plate_van']
            economic_number_part_van = data_van['economic_number']
            seats_van = data_van['seats_number']
            status_van = data_van['status']

            regex_part_eco_num = r"^(\w{2})"

            math_part_eco_num = re.match(regex_part_eco_num, economic_number_part_van, re.M | re.I)

            if math_part_eco_num:

                economic_van_number = get_economic_number_van(economic_number_part_van)

                status_valid = validate_status_applied(status_van)

            logger.info('Data to update Van: %s',
                        "UUID Van: {0}, Plate Van: {1}, Economic Number Van: {2}".format(uuid_van,
                                                                                         plates_van,
                                                                                         economic_van_number))

            json_data = dict()

            if status_valid:

                json_data = update_van_data(uuid_van, plates_van, economic_van_number, seats_van, status_van)

                logger.info('Van updated Info: %s', str(json_data))

                return json_data

        elif request.method == 'DELETE':
            data = request.get_json(force=True)

            uuid_van = data['uuid_van']
            plate_van = data['plate_van']

            logger.info('Van data to Delete: %s', 'UUID_Van: {}, Plate_Van: {}'.format(uuid_van, plate_van))

            json_data = []

            if not uuid_van and not plate_van:
                return request_conflict()

            json_data = delete_van_vehicle(uuid_van, plate_van)

            logger.info('Van delete: %s', json_data)

            return json.dumps(json_data)

        else:
            return not_found()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'error_code': 404,
        'error_message': 'Page Not Found: ' + request.url,
    }

    resp = jsonify(message)
    resp.status_code = 404

    return resp


@app.errorhandler(500)
def server_error(error=None):
    message = {
        'error_code': 500,
        'error_message': 'Server Error: ' + request.url,
    }

    resp = jsonify(message)
    resp.status_code = 500

    return resp


@app.errorhandler(401)
def request_unauthorized(error=None):
    message = {
        'error_code': 401,
        'error_message': 'Request Unauthorized: ' + request.url,
    }

    resp = jsonify(message)
    resp.status_code = 401

    return resp


@app.errorhandler(409)
def request_conflict(error=None):
    message = {
        "error_code": 409,
        "error_message": 'Request data conflict or Authentication data conflict, please verify it. ' + request.url,
    }

    resp = jsonify(message)
    resp.status_code = 409

    return resp


@app.route('/api/urbvan/authorization/', methods=['POST', 'OPTIONS'])
def get_authentication():

    json_token = {}

    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Access-Control-Max-Age': 1000,
            'Access-Control-Allow-Headers': 'origin, x-csrftoken, content-type, accept',
        }
        return '', 200, headers

    elif request.method == 'POST':
        data = request.get_json(force=True)

        user_name = data['username']
        password = data['password']
        rfc = data['rfc_client']

        regex_email = r"^[(a-z0-9\_\-\.)]+@gmail.com"

        regex_passwd = r"^[(A-Za-z0-9\_\-\.\$\#\&\*)(A-Za-z0-9\_\-\.\$\#\&\*)]+"

        match_email = re.match(regex_email, user_name, re.M | re.I)

        math_passwd = re.match(regex_passwd, password, re.M | re.I)

        if match_email and 'MOMJ880813' in rfc and math_passwd:

            password = sha256.encrypt(password + '_' + rfc)

            json_token = user_registration(user_name, password)

            json_token = json.dumps(json_token)

            return json_token

        else:
            return request_conflict()
    else:
        return not_found()


def decimal_formatting(value):
    return ('%.2f' % value).rstrip('0').rstrip('.')


def validate_status_applied(status_van):

    status_valid = False

    cfg = get_config_constant_file()

    list_van_status_applied = cfg['VAN_STATUS_CHECK_LIST']

    if status_van in list_van_status_applied:
        status_valid = True

    return status_valid


# Define y obtiene el configurador para las constantes del sistema:
def get_config_constant_file():
    """Contiene la obtencion del objeto config
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


if __name__ == "__main__":
    app.debug = True

    app.run()

