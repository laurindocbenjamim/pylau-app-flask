
from flask import Request

def __get_cookies(request: Request):
    return {
             'USERNAME': request.cookies.get('USERNAME', ''),
        'USER_STATUS': request.cookies.get('USER_STATUS', ''),
        'USER_ROLE': request.cookies.get('USER_ROLE', ''),
        'USER_TOKEN': request.cookies.get('USER_TOKEN', '')
        }
    