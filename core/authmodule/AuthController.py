
from core import User

# create a User
def create_user(db, username, password):
    object = User(username=username, password=password)
    db.session.add(object)
    db.session.commit()
    return object

# select all people
def get_users(db):
    #user = db.session.query(User).all()
    user = [user.to_dict() for user in User.query.all()]

    return user

# filter people by id
def get_user_by_id(db,id):
    #pers = db.session.execute(db.select(user).order_by(User.firstname)).scalars()
    user = User.query.filter_by(userID=id).first()
    user = db.get_or_404(User, id)
    return user.to_dict()

def check_email_exist(email):
    user = User.query.filter_by(email=email).first()
    if user:
        return True
    return False

# update a User
def update_user(db, username, password, id):
    user = User.query.get(id)
    if user:
        user.username = username
        user.password = password
        db.session.commit()
        return user.to_dict()
    else:
        return None

# delete a User
def delete_user(db, id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return user.to_dict()
    else:
        return None
