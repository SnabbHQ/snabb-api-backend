from rest_framework import status


def get_response(code):
    return responses[code]


responses = {
    200205: {
        'data': {
            'code': 200205,
            'message': 'Quote created',
            'key': 'CREATED_QUOTE'
        },
        'status': status.HTTP_200_OK
    },
    200206: {
        'data': {
            'code': 200206,
            'message': 'Address valid',
            'key': 'ADDRESS_OK'
        },
        'status': status.HTTP_200_OK
    },
    400300: {
        'data': {
            'code': 400300,
            'message': 'Tasks is required',
            'key': 'TASKS_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400301: {
        'data': {
            'code': 400301,
            'message': 'Task first_name is required',
            'key': 'TASK_FIRST_NAME_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400302: {
        'data': {
            'code': 400302,
            'message': 'Task last_name is required',
            'key': 'TASK_LAST_NAME_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400303: {
        'data': {
            'code': 400303,
            'message': 'Task company_name is required',
            'key': 'TASK_COMPANY_NAME_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400304: {
        'data': {
            'code': 400304,
            'message': 'Task phone is required',
            'key': 'TASK_PHONE_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400305: {
        'data': {
            'code': 400305,
            'message': 'Task email is required',
            'key': 'TASK_EMAIL_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400306: {
        'data': {
            'code': 400306,
            'message': 'Task address is required',
            'key': 'TASK_ADDRESS_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400307: {
        'data': {
            'code': 400307,
            'message': 'Task coordinates is required',
            'key': 'TASK_COORDINATES_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400308: {
        'data': {
            'code': 400308,
            'message': 'Task zipcode is required',
            'key': 'TASK_ZIPCODE_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400309: {
        'data': {
            'code': 400309,
            'message': 'Task city is required',
            'key': 'TASK_CITY_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400310: {
        'data': {
            'code': 400310,
            'message': 'Task order is required',
            'key': 'TASK_ORDER_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400311: {
        'data': {
            'code': 400311,
            'message': 'Invalid task type',
            'key': 'TASK_TYPE_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400401: {
        'data': {
            'code': 400401,
            'message': 'Key address is required',
            'key': 'KEY_ADDRESS_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400402: {
        'data': {
            'code': 400402,
            'message': 'Route is required',
            'key': 'ROUTE_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400403: {
        'data': {
            'code': 400403,
            'message': 'Country not valid',
            'key': 'INVALID_COUNTRY'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400404: {
        'data': {
            'code': 400404,
            'message': 'Region not valid',
            'key': 'INVALID_REGION'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400405: {
        'data': {
            'code': 400405,
            'message': 'Zipcode not valid',
            'key': 'INVALID_ZIPCODE'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400406: {
        'data': {
            'code': 400406,
            'message': 'City not valid',
            'key': 'INVALID_CITY'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400407: {
        'data': {
            'code': 400407,
            'message': 'Invalid Address',
            'key': 'INVALID_ADDRESS'
        },
        'status': status.HTTP_400_BAD_REQUEST
    }
}
