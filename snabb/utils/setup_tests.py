from snabb.users.models import Profile
from snabb.location.models import Zipcode, City, Country, Region
from snabb.deliveries.models import Delivery
"""
We use this library to setup all object creation, to use them accross our tests
"""


def create_profile():
    profile = Profile.objects.get_or_create(
        company_name='My Company S.L.', email='email@example.com',
        password='123456', phone='+34123456789', user_lang='es'
    )
    return profile[0]


def create_country(name, iso_code, active):
    country = Country.objects.get_or_create(
        name=name, iso_code=iso_code, active=active
    )
    return country[0]


def create_region(name, google_short_name, region_country, active):
    region = Region.objects.get_or_create(
        name=name, active=active,
        google_short_name=google_short_name
    )
    return region[0]


def create_zipcode(code, city, active):
    zipcode = Zipcode.objects.get_or_create(
        code=code, zipcode_city=city, active=active
    )
    return zipcode[0]


def create_city(name, google_short_name, region, active):
    city = City.objects.get_or_create(
        name=name, active=active,
        google_short_name=google_short_name,
    )
    return city[0]


def init_data_geo():
    country = create_country('Spain', 'ES', True)
    region_valencia = create_region(
        'Valencia', 'Comunidad Valenciana', country, True)
    city = create_city(
        'Albaida', 'Albaida', region_valencia, True)
    zipcode = create_zipcode(46860, city, True)


def update_delivery_status(pk, status):
    "Change delivery status for testing purposes"
    delivery = Delivery.objects.get(pk=pk)
    delivery.status = status
    delivery.save()
    return delivery