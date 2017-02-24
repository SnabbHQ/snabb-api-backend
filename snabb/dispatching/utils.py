# -*- coding: utf-8 -*-

'''
    - Dispatching APP.
'''
from django.conf import settings
from snabb.dispatching.onfleet import Onfleet
from snabb.geo_utils.utils import _get_real_eta


def _get_eta(lat, lon):
    on = Onfleet()
    workers = on._get_workers_by_location(lat, lon)

    small_vehicles = ['CAR', 'MOTORCYCLE', 'BICYCLE', 'TRUCK']
    medium_vehicles = ['CAR', 'MOTORCYCLE', 'BICYCLE', 'TRUCK']
    big_vehicles = ['CAR', 'TRUCK']

    for worker in workers['workers']:
        worker_vehicle = worker['vehicle']['type']
        worker_lon = worker['location'][0]
        worker_lat = worker['location'][1]

        small_eta = 0
        medium_eta = 0
        big_eta = 0
        # Only workers onDuty without active task.
        if worker['onDuty'] and worker['activeTask'] == None:
            if worker_vehicle == 'BICYCLE':
                mode = 'bicycling'
            else:
                mode = 'driving'

            current_worker_eta = _get_real_eta(
                    worker_lat,
                    worker_lon,
                    lat,
                    lon,
                    mode
                    )
            if worker_vehicle in small_vehicles:
                if small_eta == 0:
                    # Only save if we don't have a better eta for this size.
                    small_eta = current_worker_eta
            if worker_vehicle in medium_vehicles:
                if medium_eta == 0:
                    # Only save if we don't have a better eta for this size.
                    medium_eta = current_worker_eta
            if worker_vehicle in big_vehicles:
                if big_eta == 0:
                    # Only save if we don't have a better eta for this size.
                    big_eta = current_worker_eta

            '''
            if small_eta > 0 and medium_eta > 0 and big_eta > 0:
                # If we have the three ETAs, we dont need any more info.
                break
            '''
    '''
    Coche -> Todos
    Furgoneta -> Todos
    Moto -> Mediano - pequeño
    Bicicleta -> Mediano - pequeño
    A pie -> Pequeños (edited)
    '''

    etas = {
        'small': small_eta,
        'medium': medium_eta,
        'big': big_eta
    }
    return etas
