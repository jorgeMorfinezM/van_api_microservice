# -*- coding: utf-8 -*-
"""
Requires Python 3.0 or later
"""

__author__ = "Jorge Morfinez Mojica (jorge.morfinez.m@gmail.com)"
__copyright__ = "Copyright 2020, Jorge Morfinez Mojica"
__license__ = ""
__history__ = """ """
__version__ = "1.1.L31.2 ($Rev: 5 $)"

from flask import Flask, jsonify, make_response, \
    url_for, redirect, render_template, json, request, Response, url_for, flash, redirect, session
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)
from flask_jwt_extended import JWTManager
from auth_controller.api_authentication import *
from constants.constants import Constants as Const
from logger_controller.logger_control import *
from db_controller.database_backend import *
from functools import wraps
import threading
import time
import json
import re


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


def get_orders_by_order_id(order_id, order_type):
    pass

    database_cnx_data = []

    session = session_to_db()

    orders_header_list = []

    cfg = get_config_constant_file()

    table_name = cfg['DB_ORACLE_OBJECTS']['ORDER_H']

    try:

        database_cnx_data = init_connection_data()

        orders_list = select_orders_header(session, table_name, order_id, order_type)

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

    orders_header_list = json.loads(orders_list)

    if len(orders_header_list) != 0:

        print('Order Data Header: ', orders_header_list)

        return orders_header_list


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
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
                'Access-Control-Max-Age': 1000,
                'Access-Control-Allow-Headers': 'origin, x-csrftoken, content-type, accept',
            }
            return '', 200, headers

        elif request.method == 'GET':

            data = request.get_json(force=True)

            order_id = data['order_id']

            json_data = []

            json_data = get_orders_by_order_id(order_id)

            if not order_id:
                return request_conflict()

            return json.dumps(json_data)

        else:
            return not_found()


def get_order_status_by_id(order_id, order_type):

    database_cnx_data = []

    session = session_to_db()

    status_order = []

    cfg = get_config_constant_file()

    table_name = cfg['DB_ORACLE_OBJECTS']['ORDER_H']

    try:
        database_cnx_data = init_connection_data()

        order_status = select_status_order_by_id(session, table_name, order_id, order_type)

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

    status_order = json.loads(order_status)

    if len(status_order) != 0:
        logger.info('Status Order: %s', str(status_order))

        return status_order


def update_order_status_by_id(order_id, order_type, order_status):

    database_cnx_data = []

    session = session_to_db()

    status_ok = []

    cfg = get_config_constant_file()

    table_name = cfg['DB_ORACLE_OBJECTS']['ORDER_H']

    try:
        database_cnx_data = init_connection_data()

        status_updated = update_status_order_by_id(session, table_name, order_id, order_type, order_status)

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

    status_ok = json.loads(status_updated)

    if len(status_ok) != 0:
        logger.info('Status Order Updated: %s', str(status_ok))

        return status_ok


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
                'Access-Control-Allow-Origin': '*',
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

            json_order_response = manage_order_integration_data(data)

            return json.dumps(json_order_response)

            # return json.dumps(json_order_response)

        elif request.method == 'GET':
            data = request.get_json(force=True)

            logger.info('Data to get Order Status: %s', 'OrderId: {}, Order_Type: {}'.format(data['order_id'],
                                                                                             data['order_type']))

            order_id = data['order_id']
            order_type = data['order_type']

            json_data = []

            if not order_id and not order_type:
                return request_conflict()

            json_data = get_order_status_by_id(order_id, order_type)

            logger.info('Order Status Info: %s', json_data)

            return json.dumps(json_data)

        elif request.method == 'PUT':

            status_order_updated = 'FAIL'

            data = request.get_json(force=True)

            logger.info('Data to get Order Status: %s',
                        "OrderId: {0}, Order_Type: {1}, Status: {2}".format(data['OrderId'],
                                                                            data['TipoPedido'],
                                                                            data['StatusPedido']))

            order_id = data['OrderId']
            order_type = data['TipoPedido']
            order_status = data['StatusPedido']

            json_data = []

            if not order_id and not order_type and not order_status:
                return request_conflict()

            json_data = update_order_status_by_id(order_id, order_type, order_status)

            json_data_from_bd = json.dumps(json_data)
            json_data_from_bd_loads = json.loads(json_data_from_bd)

            for data_status in json_data_from_bd_loads:

                data_status_dumps = json.dumps(data_status)
                data_status_loads = json.loads(data_status_dumps)

                status_order_updated = '{}'.format(data_status_loads["StatusOK"])

                if 'OK' in status_order_updated:

                    logger.info('Order Status Info: %s', str(json_data_from_bd))

                    return json_data_from_bd

        elif request.method == 'DELETE':
            pass

        else:
            return not_found()


def manage_order_integration_data(data_order_integration):

    database_cnx_data = []

    session = session_to_db()

    order_integrator_response = []

    try:

        database_cnx_data = init_connection_data()

        tipo_pedido = data_order_integration['tipo_pedido']
        order_id = data_order_integration['order_id']
        id_pedido_integrador = data_order_integration['id_pedido_integrador']
        estatus_envio = data_order_integration['estatus_envio']
        origen_envio = data_order_integration['origen_envio']
        observaciones_request = data_order_integration['observaciones_request']
        integrador_id = data_order_integration['integrador_id']
        created_by = data_order_integration['created_by']
        last_updated_by = data_order_integration['last_updated_by']

        response_order = PedidosIntegracionApi.manage_pedidos_integracion_api(session, tipo_pedido, order_id,
                                                                              id_pedido_integrador, estatus_envio,
                                                                              origen_envio, observaciones_request,
                                                                              integrador_id, created_by,
                                                                              last_updated_by)

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

    order_integrator_response = json.loads(response_order)

    if len(order_integrator_response) != 0:

        logger.info('Response Order Integrator BD: %s', str(order_integrator_response))

        return order_integrator_response


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
            'Access-Control-Allow-Origin': '*',
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

            password = password + '_' + rfc

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

