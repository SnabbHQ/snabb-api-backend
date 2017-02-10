from rest_framework import status


def get_response(code):
    return responses[code]


responses = {
    400306: {
        'data': {
            'code': 400306,
            'message': 'Pickup address is required',
            'key': 'PICKUP_ADDRESS_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400301: {
        'data': {
            'code': 400301,
            'message': 'Pickup first_name is required',
            'key': 'PICKUP_FIRST_NAME_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400302: {
        'data': {
            'code': 400302,
            'message': 'Pickup last_name is required',
            'key': 'PICKUP_LAST_NAME_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400303: {
        'data': {
            'code': 400303,
            'message': 'Pickup company_name is required',
            'key': 'PICKUP_COMPANY_NAME_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400303: {
        'data': {
            'code': 400304,
            'message': 'Pickup phone is required',
            'key': 'PICKUP_PHONE_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400305: {
        'data': {
            'code': 400305,
            'message': 'Pickup email is required',
            'key': 'PICKUP_EMAIL_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400306: {
        'data': {
            'code': 400306,
            'message': 'Pickup address is required',
            'key': 'PICKUP_ADDRESS_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400307: {
        'data': {
            'code': 400307,
            'message': 'Pickup coordinates is required',
            'key': 'PICKUP_COORDINATES_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400308: {
        'data': {
            'code': 400308,
            'message': 'Pickup zipcode is required',
            'key': 'PICKUP_ZIPCODE_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400309: {
        'data': {
            'code': 400309,
            'message': 'Pickup city is required',
            'key': 'PICKUP_CITY_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400311: {
        'data': {
            'code': 400311,
            'message': 'Dropoff first_name is required',
            'key': 'DROPOFF_FIRST_NAME_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400312: {
        'data': {
            'code': 400312,
            'message': 'Dropoff last_name is required',
            'key': 'DROPOFF_LAST_NAME_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400313: {
        'data': {
            'code': 400313,
            'message': 'Dropoff company_name is required',
            'key': 'DROPOFF_COMPANY_NAME_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400314: {
        'data': {
            'code': 400314,
            'message': 'Dropoff phone is required',
            'key': 'DROPOFF_PHONE_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400315: {
        'data': {
            'code': 400315,
            'message': 'Dropoff email is required',
            'key': 'DROPOFF_EMAIL_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400316: {
        'data': {
            'code': 400316,
            'message': 'Dropoff address is required',
            'key': 'DROPOFF_ADDRESS_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400317: {
        'data': {
            'code': 400317,
            'message': 'Dropoff coordinates is required',
            'key': 'DROPOFF_COORDINATES_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400318: {
        'data': {
            'code': 400318,
            'message': 'Dropoff zipcode is required',
            'key': 'DROPOFF_ZIPCODE_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400319: {
        'data': {
            'code': 400319,
            'message': 'Dropoff city is required',
            'key': 'DROPOFF_CITY_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400210: {
        'data': {
            'code': 400210,
            'message': 'Invalid Address',
            'key': 'INVALID_ADDRESS'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    200205: {
        'data': {
            'code': 200205,
            'message': 'Quote created',
            'key': 'CREATED_QUOTE'
        },
        'status': status.HTTP_200_OK
    },
}
