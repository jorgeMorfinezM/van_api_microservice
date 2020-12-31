# -*- coding: utf-8 -*-
"""
Requires Python 3.8 or later
"""

__author__ = "Jorge Morfinez Mojica (jorge.morfinez.m@gmail.com)"
__copyright__ = "Copyright 2020, Jorge Morfinez Mojica"
__license__ = ""
__history__ = """ """
__version__ = "1.1.L31.2 ($Rev: 1 $)"

from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)
from db_controller.database_backend import *


logger = configure_ws_logger()


def generate_hash(password):
    return sha256.hash(password)


def verify_hash(password, hash):
    return sha256.verify(password, hash)


def user_registration(user_name, user_password):

    password_hash = generate_hash(user_password)

    try:

        if verify_hash(user_password, password_hash):

            access_token = create_access_token(identity=user_name)

            refresh_token = create_refresh_token(identity=user_name)

            UsersAuth.manage_user_authentication('', user_name, user_password, password_hash)

            logger.info('User inserted/updated in database: %s',
                        ' User_Name: "{}", Password_Hash: "{}" '.format(user_name,
                                                                        password_hash))
            return {
                'message': 'Logged in as {}'.format(user_name),
                'access_token': access_token,
                'refresh_token': refresh_token
            }

        else:
            return {'message': 'Wrong credentials'}

    except SQLAlchemyError as error:
        raise mvc_exc.ConnectionError(
            '"{}@{}" Can\'t connect to database, verify data connection to "{}".\nOriginal Exception raised: {}'.format(
                user_name, 'users_api', 'users_api', error
            )
        )
