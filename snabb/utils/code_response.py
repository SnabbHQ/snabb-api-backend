from rest_framework import status


def get_response(code):
    return responses[code]


responses = {
    200101: {
        'data': {
            'code': 200101,
            'message': 'Email verified',
            'key': 'VERIFY_OK'
        },
        'status': status.HTTP_200_OK
    },
    200102: {
        'data': {
            'code': 200102,
            'message': 'Email Sended',
            'key': 'SEND_EMAIL_OK'
        },
        'status': status.HTTP_200_OK
    },
    200103: {
        'data': {
            'code': 200103,
            'message': 'Password Updated',
            'key': 'PASSWORD_UPDATE_OK'
        },
        'status': status.HTTP_200_OK
    },
    200104: {
        'data': {
            'code': 200104,
            'message': 'Password reset',
            'key': 'RESET_OK'
        },
        'status': status.HTTP_200_OK
    },
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
    200207: {
        'data': {
            'code': 200207,
            'message': 'Charge successful',
            'key': 'CHARGE_OK'
        },
        'status': status.HTTP_200_OK
    },
    400101: {
        'data': {
            'code': 400101,
            'message': 'Invalid email',
            'key': 'EMAIL_WRONG'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400102: {
        'data': {
            'code': 400102,
            'message': 'Password must be at least 6 chars long.',
            'key': 'PASSWORD_WRONG'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400103: {
        'data': {
            'code': 400101,
            'message': 'Email already exists',
            'key': 'EMAIL_ALREADY_EXISTS'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400104: {
        'data': {
            'code': 400104,
            'message': 'Company Name, Email, phone and password required',
            'key': 'EMAIL_AND_PASSWORD_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400105: {
        'data': {
            'code': 400105,
            'message': 'User hash required',
            'key': 'HASH_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400106: {
        'data': {
            'code': 400106,
            'message': 'Hash not exists',
            'key': 'HASH_NOT_EXISTS'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400107: {
        'data': {
            'code': 400107,
            'message': 'This user is already verified',
            'key': 'ALREADY_VERIFIED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400108: {
        'data': {
            'code': 400108,
            'message': 'An error has occurred',
            'key': 'VERIFY_ERROR'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400109: {
        'data': {
            'code': 400109,
            'message': 'Email required',
            'key': 'EMAIL_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400110: {
        'data': {
            'code': 400110,
            'message': 'Email not exists',
            'key': 'EMAIL_NOT_EXISTS'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400111: {
        'data': {
            'code': 400111,
            'message': 'This user is already verified',
            'key': 'ALREADY_VERIFIED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400112: {
        'data': {
            'code': 400112,
            'message': 'Wrong current password.',
            'key': 'CURRENT_PASSWORD_WRONG'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400113: {
        'data': {
            'code': 400113,
            'message': 'current_password and new_password required.',
            'key': 'REQUIRED_FIELDS'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400114: {
        'data': {
            'code': 400114,
            'message': 'User hash and password required',
            'key': 'HASH_PASSWORD_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
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
    },
    400501: {
        'data': {
            'code': 400501,
            'message': 'Receipt User does not exist',
            'key': 'INVALID_RECEIPT_USER'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400502: {
        'data': {
            'code': 400502,
            'message': 'Receipt Courier does not exist',
            'key': 'INVALID_RECEIPT_COURIER'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400503: {
        'data': {
            'code': 400503,
            'message': 'Quote ID required',
            'key': 'QUOTE_ID_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400504: {
        'data': {
            'code': 400504,
            'message': 'Package size required',
            'key': 'PACKAGE_SIZE_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400506: {
        'data': {
            'code': 400506,
            'message': 'Quote not exists',
            'key': 'QUOTE_NOT_EXISTS'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400507: {
        'data': {
            'code': 400507,
            'message': 'Expired quote',
            'key': 'EXPIRED_QUOTE'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400600: {
        'data': {
            'code': 400600,
            'message': 'Token is required',
            'key': 'TOKEN_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400601: {
        'data': {
            'code': 400601,
            'message': 'Delivery_id is required',
            'key': 'DELIVERY_ID_REQUIRED'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400602: {
        'data': {
            'code': 400602,
            'message': 'Delivery does not exists',
            'key': 'DELIVERY_NOT_EXISTS'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400603: {
        'data': {
            'code': 400603,
            'message': 'Error creating Customer Stripe',
            'key': 'CUSTOMER_STRIPE_ERROR'
        },
        'status': status.HTTP_400_BAD_REQUEST
    },
    400604: {
        'data': {
            'code': 400604,
            'message': 'Error creating Card Stripe',
            'key': 'CARD_STRIPE_ERROR'
        },
        'status': status.HTTP_400_BAD_REQUEST
    }
}
