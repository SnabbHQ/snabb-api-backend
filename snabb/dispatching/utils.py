# -*- coding: utf-8 -*-

'''
    - Dispatching APP.
'''
from django.conf import settings
from snabb.dispatching.onfleet import Onfleet
from snabb.geo_utils.utils import _check_distance_between_points


def _get_eta(lat, lon):
    on = Onfleet()
    workers = on._get_workers_by_location(lat, lon)

    small_vehicles = ['CAR', 'MOTORCYCLE', 'BICYCLE', 'TRUCK']
    medium_vehicles = ['CAR', 'MOTORCYCLE', 'BICYCLE', 'TRUCK']
    big_vehicles = ['CAR', 'TRUCK']

    for worker in workers['workers']:
        print('----')
        print (worker)
        print('----')
        worker_vehicle = worker['vehicle']['type']
        worker_lon = worker['location'][0]
        worker_lat = worker['location'][1]
        print(worker_lon)
        print(worker_lat)
        if worker_vehicle in small_vehicles:
            distance = _check_distance_between_points(
                    lat,
                    lon,
                    worker_lat,
                    worker_lon
                    )
    '''
        https://maps.googleapis.com/maps/api/directions/json?origin=Juan%20Verdeguer,%2016,%20Valencia,%20España&destination=PAsaje%20Doctor%20Serra,%203,%2046004,%20Valencia&key=AIzaSyBenCk9al8Bj5Gms0-G11Ug1jaKt0sf2mo&mode=bicycling
    '''
    '''
    _check_distance_between_points(
        origin_latitude,
        origin_longitude,
        current_latitude,
        current_longitude
        )

    Coche -> Todos
    Furgoneta -> Todos
    Moto -> Mediano - pequeño
    Bicicleta -> Mediano - pequeño
    A pie -> Pequeños (edited)
    '''
    small_eta = 0
    medium_eta = 0
    big_eta = 0
    etas = {
        'small': small_eta,
        'medium': medium_eta,
        'big': big_eta
    }
    return etas
