# -*- coding: utf-8 -*-

'''
    - Dispatching APP.
'''
from django.conf import settings
from snabb.dispatching.onfleet import Onfleet
from snabb.geo_utils.utils import _get_real_eta, _get_location_info


def _get_eta(lat, lon):
    on = Onfleet()
    workers = on._get_workers_by_location(lat, lon)

    small_vehicles = ['CAR', 'MOTORCYCLE', 'BICYCLE', 'TRUCK']
    medium_vehicles = ['CAR', 'MOTORCYCLE', 'BICYCLE', 'TRUCK']
    big_vehicles = ['CAR', 'TRUCK']

    small_eta = "0"
    medium_eta = "0"
    big_eta = "0"

    if workers is not None:
        for worker in workers['workers']:
            if worker['vehicle'] is not None:
                # Check if current worker have vehicle, if not, pass.
                worker_vehicle = worker['vehicle']['type']
                worker_lon = worker['location'][0]
                worker_lat = worker['location'][1]

                # Only workers onDuty without active task.
                if worker['onDuty'] and worker['activeTask'] is None:
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
                        if small_eta == "0":
                            # Only save if we don't have a better eta for this
                            # size.
                            small_eta = current_worker_eta
                    if worker_vehicle in medium_vehicles:
                        if medium_eta == "0":
                            # Only save if we don't have a better eta for this
                            # size.
                            medium_eta = current_worker_eta
                    if worker_vehicle in big_vehicles:
                        if big_eta == "0":
                            # Only save if we don't have a better eta for this
                            # size.
                            big_eta = current_worker_eta

                    if small_eta != "0" and medium_eta != "0" and big_eta != "0":
                        # If we have the three ETAs, we dont need any more
                        # info.
                        break
            else:
                pass

    etas = {
        'small': small_eta,
        'medium': medium_eta,
        'big': big_eta
    }
    return etas


def _get_available_workers_by_location(lat, lon, package_size):
    '''
    This function gets a lat lon, and package_size.
    And return the closest worker for this location
    '''
    available_vehicles = {}
    available_vehicles['small'] = ['CAR', 'MOTORCYCLE', 'BICYCLE', 'TRUCK']
    available_vehicles['medium'] = ['CAR', 'MOTORCYCLE', 'BICYCLE', 'TRUCK']
    available_vehicles['big'] = ['CAR', 'TRUCK']

    on = Onfleet()
    workers = on._get_workers_by_location(lat, lon)
    # Return only workers onDuty without active task and with vehicle.
    if workers is not None:
        for worker in workers['workers']:
            if (worker['vehicle'] is not None and worker['onDuty']
                    and worker['activeTask'] is None):
                worker_vehicle = worker['vehicle']['type']
                # Check if current worker vehicle is in our selected package
                # size
                if worker_vehicle in available_vehicles[package_size]:
                    return worker['id']
                else:
                    pass
            else:
                pass
    else:
        return None

# Team related functions


def _create_team(team_name):
    on = Onfleet()
    new_team = on._create_team(team_name)
    return new_team


def _update_team(team_name, team_id):
    on = Onfleet()
    updated_team = on._update_team(team_name, team_id)
    return updated_team


def _delete_team(team_id):
    on = Onfleet()
    deleted_team = on._delete_team(team_id)
    return deleted_team


def _get_team_detail(team_id):
    on = Onfleet()
    detail_team = on._get_team_detail(team_id)
    return detail_team


def _get_all_teams():
    on = Onfleet()
    all_teams = on._get_all_teams()
    return all_teams


# Courier related functions
def _create_worker(name, phone, teams):
    on = Onfleet()
    new_courier = on._create_worker(name, phone, teams)
    return new_courier


def _get_worker_detail(worker_id):
    on = Onfleet()
    detail_courier = on._get_worker_detail(worker_id)
    return detail_courier


def _update_worker(worker_id, name=None, teams=None):
    on = Onfleet()
    updated_courier = on._update_worker(worker_id, name, teams)
    return updated_courier


def _delete_worker(worker_id):
    on = Onfleet()
    deleted_courier = on._delete_worker(worker_id)
    return deleted_courier


def _get_all_workers():
    on = Onfleet()
    all_workers = on._get_all_workers()
    return all_workers


# Tasks related functions
def _create_task(destination, recipients, notes, dependencies,
                 pickupTask=False, completeAfter=None, completeBefore=None,
                 container=None):

    on = Onfleet()
    new_task = on._create_task(destination, recipients, notes, dependencies,
                               pickupTask, completeAfter, completeBefore,
                               container)
    return new_task


def _get_task_detail(task_id):
    on = Onfleet()
    detail_task = on._get_task_detail(task_id)
    return detail_task


def _assign_task(task_id, worker_id):
    on = Onfleet()
    assigned_task = on._assign_task(task_id, worker_id)
    return assigned_task


def _delete_task(task_id):
    on = Onfleet()
    deleted_task = on._delete_task(task_id)
    return deleted_task


def _send_dispatching(task, task_id=None):
    "We use this function to create task in Onfleet, and link dependencies."
    if not task.task_onfleet_id:
        try:
            location_info = _get_location_info(
                task.task_place.place_address.address)

            address = {}
            address['number'] = location_info['street_number']
            address['street'] = location_info['route']
            address['city'] = location_info['city']
            address['state'] = location_info['region']
            address['country'] = location_info['country']
            destination = {
                'address': address,
                # {"unparsed": task.task_place.place_address.address},
                'notes': task.task_place.description
            }
            notes = task.comments
            recipients = []
            # If contact doesn't have name, we use company_name
            if task.task_contact.first_name and task.task_contact.last_name:
                name = task.task_contact._get_full_name()
                if task.task_contact.company_name:
                    comments = task.comments + ' ' + task.task_contact.company_name
                else:
                    comments = task.comments
            else:
                name = task.task_contact.company_name
                comments = task.comments
            recipient = {"name": name,
                         "phone": task.task_contact.phone,
                         "notes": comments}
            recipients.append(recipient)

            if task.task_type == 'pickup':
                pickupTask = True
            else:
                pickupTask = False

            dependencies = []
            if task_id is not None:
                dependencies.append(task_id)

            # Create task in onfleet.
            new_task = _create_task(destination, recipients,
                                    notes, dependencies, pickupTask)

            return new_task
        except Exception as error:
            print(error)
            return None
    else:
        # Already exists at onfleet
        task_detail = _get_task_detail(task.task_onfleet_id)
        return task_detail
