import flask

from .createViews.createView import CreateView

from flask_login import LoginManager



bp = flask.Blueprint('createUser', __name__, url_prefix='/create-user', template_folder='templates')

def init_app(login_manager, db):
    
    from ..model.users import Users

    @login_manager.user_loader
    def load_user(email):
        return Users.query.get(email)
        if len(users) > 0:
            user = [u for u in users if u['email'] == email]
            if not user:
                return 
            return user[0]
        return  

    bp.add_url_rule('/new-user', view_func=CreateView.as_view('newUser', Users,  template='create.html'))
# Last block of code in the file
"""

login_manager = LoginManager()
# Initialize the login_manager with the Flask app object
login_manager.init_app(bp)

from ..model.users import Users

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

bp.add_url_rule('/new', view_func=CreateView.as_view('create', Users,  template='create.html'))

"""



"""
@bp.route('/new', methods=['GET', 'POST'])
def create():
    if flask.request.method == 'POST':
        Users.create_user(flask.request.form)
        #flash('User created successfully')
        return {'message':'User created successfully'}
    #return flask.render_template('create.html', title='Create User')
    return {'message':'Create User'}

"""


"""
When I call the template 'create.html' I get the error: AttributeError: 'Flask' object has no attribute 'login_manager'
"""
