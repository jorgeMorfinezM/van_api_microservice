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


def insert_order_header(json_data_head):

    database_cnx_data = []

    session = session_to_db()

    order_header_response = []

    try:
        database_cnx_data = init_connection_data()

        tipo_pedido = json_data_head['tipo_pedido']
        orderid = json_data_head['orderid']
        orderguid = json_data_head['orderguid']
        orderstatusid = json_data_head['orderstatusid']
        paymentstatusid = json_data_head['paymentstatusid']
        shippingstatusid = json_data_head['shippingstatusid']
        customerlanguageid = json_data_head['customerlanguageid']
        customertaxdisplaytypeid = json_data_head['customertaxdisplaytypeid']
        ordersubtotalincltax = json_data_head['ordersubtotalincltax']
        ordersubtotalexcltax = json_data_head['ordersubtotalexcltax']
        ordersubtotaldiscountincltax = json_data_head['ordersubtotaldiscountincltax']
        ordersubtotaldiscountexcltax = json_data_head['ordersubtotaldiscountexcltax']
        ordershippingincltax = json_data_head['ordershippingincltax']
        ordershippingexcltax = json_data_head['ordershippingexcltax']
        paymethodaddfeeincltax = json_data_head['paymethodaddfeeincltax']
        paymethodaddfeeexcltax = json_data_head['paymethodaddfeeexcltax']
        taxrates = json_data_head['taxrates']
        ordertax = json_data_head['ordertax']
        ordertotal = json_data_head['ordertotal']
        refundedamount = json_data_head['refundedamount']
        orderdiscount = json_data_head['orderdiscount']
        currencyrate = json_data_head['currencyrate']
        customercurrencycode = json_data_head['customercurrencycode']
        affiliateid = json_data_head['affiliateid']
        affiliateurlfliendly = json_data_head['affiliateurlfliendly']
        vatnumber = json_data_head['vatnumber']
        usocfdi = json_data_head['usocfdi']
        billingfirstname = json_data_head['billingfirstname']
        billinglastname = json_data_head['billinglastname']
        billingemail = json_data_head['billingemail']
        billingcrmid = json_data_head['billingcrmid']
        billingcountryid = json_data_head['billingcountryid']
        billingcountryname = json_data_head['billingcountryname']
        billingstateprovinceid = json_data_head['billingstateprovinceid']
        billingstateprovincename = json_data_head['billingstateprovincename']
        billingcity = json_data_head['billingcity']
        billingaddress1 = json_data_head['billingaddress1']
        billingaddress2 = json_data_head['billingaddress2']
        billing_entrecalles = json_data_head['billing_entrecalles']
        billing_numero_exterior = json_data_head['billing_numero_exterior']
        billingzippostalcode = json_data_head['billingzippostalcode']
        billingphonenumber = json_data_head['billingphonenumber']
        billingfaxnumber = json_data_head['billingfaxnumber']
        paymentmethodsystemname = json_data_head['paymentmethodsystemname']
        paiddateutc = json_data_head['paiddateutc']
        shippingfirstname = json_data_head['shippingfirstname']
        shippinglastname = json_data_head['shippinglastname']
        shippingemail = json_data_head['shippingemail']
        # shippingcrmid = json_data_head['shippingcrmid']
        shippingcountryid = json_data_head['shippingcountryid']
        shippingcountryname = json_data_head['shippingcountryname']
        shippingstateprovinceid = json_data_head['shippingstateprovinceid']
        shippingstateprovincename = json_data_head['shippingstateprovincename']
        shippingcity = json_data_head['shippingcity']
        shippingaddress1 = json_data_head['shippingaddress1']
        shippingaddress2 = json_data_head['shippingaddress2']
        shipping_entrecalles = json_data_head['shippingentrecalles']
        shipping_numero_exterior = json_data_head['shipping_numero_exterior']
        shippingzippostalcode = json_data_head['shippingzippostalcode']
        shippingphonenumber = json_data_head['shippingphonenumber']
        shippingfaxnumber = json_data_head['shippingfaxnumber']
        shippingmethod = json_data_head['shippingmethod']
        shippingratecompmethodsysname = json_data_head['shippingratecompmethodsysname']
        deleted = json_data_head['deleted']
        createdonutc = json_data_head['createdonutc']
        pickupinstore = json_data_head['pickupinstore']
        agreement_id = json_data_head['agreement_id']
        customer_id = json_data_head['customer_id']
        billing_address_id = json_data_head['billing_address_id']
        shipping_address_id = json_data_head['shipping_address_id']

        order_response_header = OrderHeader.manage_orders_header(session, tipo_pedido, orderid, orderguid, orderstatusid,
                                                                 paymentstatusid, shippingstatusid, customerlanguageid,
                                                                 customertaxdisplaytypeid, ordersubtotalincltax,
                                                                 ordersubtotalexcltax, ordersubtotaldiscountincltax,
                                                                 ordersubtotaldiscountexcltax, ordershippingincltax,
                                                                 ordershippingexcltax, paymethodaddfeeincltax,
                                                                 paymethodaddfeeexcltax, taxrates, ordertax, ordertotal,
                                                                 refundedamount, orderdiscount, currencyrate,
                                                                 customercurrencycode, affiliateid, affiliateurlfliendly,
                                                                 vatnumber, usocfdi, billingfirstname, billinglastname,
                                                                 billingemail, billingcrmid, billingcountryid,
                                                                 billingcountryname, billingstateprovinceid,
                                                                 billingstateprovincename, billingcity, billingaddress1,
                                                                 billingaddress2, billingzippostalcode,
                                                                 billingphonenumber, billingfaxnumber,
                                                                 paymentmethodsystemname, paiddateutc, shippingfirstname,
                                                                 shippinglastname, shippingemail, shippingcountryid,
                                                                 shippingcountryname, shippingstateprovinceid,
                                                                 shippingstateprovincename, shippingcity,
                                                                 shippingaddress1, shippingaddress2,
                                                                 shippingzippostalcode, shippingphonenumber,
                                                                 shippingfaxnumber, shippingmethod,
                                                                 shippingratecompmethodsysname, deleted, createdonutc,
                                                                 pickupinstore, shipping_entrecalles,
                                                                 billing_entrecalles, billing_numero_exterior,
                                                                 shipping_numero_exterior, agreement_id, customer_id,
                                                                 billing_address_id, shipping_address_id)

    except SQLAlchemyError as error:
        raise mvc_exc.ConnectionError(
            '"{}@{}" Can\'t connect to database, verify data connection to "{}".\nOriginal Exception raised: {}'.format(
                database_cnx_data[1], database_cnx_data[0], database_cnx_data[4], error
            )
        )
    except TimeoutError as timeoout_error:
        raise mvc_exc.TimeoutError(
            '"{}@{}" A TimeoutError was occurred while connect to database, verify data connection to "{}".\n'
            'Original Exception raised: {}'.format(
                database_cnx_data[1], database_cnx_data[0], database_cnx_data[4], timeoout_error
            )
        )
    finally:
        session.close()

    order_header_response = json.loads(order_response_header)

    if len(order_header_response) != 0:

        logger.info('Response Order Header inserted: %s', str(order_header_response))

        return order_header_response


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

        uuid_van = data_van['uuid_van']
        plates_van = data_van['plate_van']
        economic_number_part_van = data_van['economic_number']
        seats_van = data_van['seats_number']
        status_van = data_van['status']

        regex_part_eco_num = r"^(\w{2})"

        math_part_eco_num = re.match(regex_part_eco_num, economic_number_part_van, re.M | re.I)

        if math_part_eco_num:

            economic_number_van = get_economic_number_van(economic_number_part_van)

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

            json_order_response = manage_van_requested_data(data)

            return json.dumps(json_order_response)

            # return json.dumps(json_order_response)

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

            logger.info('Data to get Order Status: %s',
                        "OrderId: {0}, Order_Type: {1}, Status: {2}".format(data['OrderId'],
                                                                            data['TipoPedido'],
                                                                            data['StatusPedido']))

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

            json_data = dict()

            if not data_van:
                return request_conflict()

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


'''
@jwt_refresh_token_required
def check_auth(username, password):

    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)

    return {'access_token': access_token}


def authenticate():
    message = {'message': "Authenticate."}
    resp = jsonify(message)

    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'Basic realm="Example"'

    return resp


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return authenticate()

        elif not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated

'''


def decimal_formatting(value):
    return ('%.2f' % value).rstrip('0').rstrip('.')


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

