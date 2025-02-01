
from flask import Request, make_response
"""
Methods to set and get the application cookies
"""


# Method to set cookies
def __set_cookies(response: make_response, current_page):
    response.set_cookie('current_page', current_page)

# method to get cookies
def __get_cookies(request: Request):
    return {
             'USERNAME': request.cookies.get('USERNAME', ''),
        'USER_STATUS': request.cookies.get('USER_STATUS', ''),
        'USER_ROLE': request.cookies.get('USER_ROLE', ''),
        'USER_TOKEN': request.cookies.get('USER_TOKEN', '')
        }
    