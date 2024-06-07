
from flask.views import View

class UserListView(View):
    methods = ['GET']

    def __init__(self):
        pass

    def dispatch_request(self):
        return [
            {'id': 1, 'name': 'lauri', 'age': '12', 'email': 'lauri@email.com'},
            {'id': 1, 'name': 'mauro', 'age': '15', 'email': 'mauro@email.com'}
        ]