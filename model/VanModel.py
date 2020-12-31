# -*- coding: utf-8 -*-
"""
Requires Python 3.8 or later
"""

__author__ = "Jorge Morfinez Mojica (jorge.morfinez.m@gmail.com)"
__copyright__ = "Copyright 2020, Jorge Morfinez Mojica"
__license__ = ""
__history__ = """ """
__version__ = "1.1.L31.2 ($Rev: 3 $)"


import datetime
import uuid


class VanModel:

    r"""
    uuid: UUID único para identificar la reserva del usuario
    plates: Placas de la VAN
    economic_number: Una nomenclatura para identificar a las camionetas.Ejemplo A1-0001
    seats: Cantidad de asientos disponibles por camioneta
    created_at: Fecha de alta de la VAN
    status: Posibles estatus de la VAN: “Activa”, “En reparación”, “Baja”
    """

    uuid = int()
    plates = str()
    economic_number = str()
    seats = int()
    created_at = datetime.datetime
    status = str()

    def __init__(self, plates, economic_number, seats, created_at, status):
        self.uuid = uuid.uuid4()
        self.plates = plates
        self.economic_number = economic_number
        self.seats = seats
        self.created_at = created_at
        self.status = status

    # getter method
    @classmethod
    def get_uuid_van(cls):
        return cls.uuid

    # setter method
    @classmethod
    def set_uuid_van(cls, uuid_van):
        cls.uuid = uuid_van

    # getter method
    @classmethod
    def get_plates_van(cls):
        return cls.plates

    # setter method
    @classmethod
    def set_plates_van(cls, plates_van):
        cls.plates = plates_van

    # getter method
    @classmethod
    def get_economic_number_van(cls):
        return cls.economic_number

    # setter method
    @classmethod
    def set_economic_number_van(cls, economic_number_van):
        cls.economic_number = economic_number_van

    # getter method
    @classmethod
    def get_seats_van(cls):
        return cls.seats

    # setter method
    @classmethod
    def set_seats_van(cls, seats_van):
        cls.seats = seats_van

    # getter method
    @classmethod
    def get_created_at(cls):
        return cls.created_at

    # setter method
    @classmethod
    def set_created_at(cls, created_at):
        cls.created_at = created_at

    # getter method
    @classmethod
    def get_status_van(cls):
        return cls.status

    # setter method
    @classmethod
    def set_status_van(cls, status_van):
        cls.status = status_van
