
from core import User
from datetime import datetime
from flask import jsonify

# create a User
def create_user(db, firstname, lastname, email, country,
        country_code, phone, password, two_factor_auth_secret=None, status='inactive'):
    object = User( 
        firstname = firstname,
        lastname = lastname,
        email = email,
        country = country,
        country_code = country_code,
        phone = phone,
        password = password,
        two_factor_auth_secret = two_factor_auth_secret,
        date_updated = datetime.now()
    )
    db.session.add(object)
    db.session.commit()
    return object.to_dict()

# select all people
def get_users(db):
    #user = db.session.query(User).all()
    user = [user.to_dict() for user in User.query.all()]

    return user

# filter people by id
def get_user_by_id(db,id):
    #pers = db.session.execute(db.select(user).order_by(User.firstname)).scalars()
    user = User.query.filter_by(userID=id).first()
    
    return user.to_dict()

def get_user_by_id_limited_dict(db,id):
    #pers = db.session.execute(db.select(user).order_by(User.firstname)).scalars()
    user = User.query.filter_by(userID=id).first()
   
    return user.to_limited_dict()

def _get_user_by_id(id):
    try:
        #pers = db.session.execute(db.select(user).order_by(User.firstname)).scalars()
        user = User.query.filter_by(userID=id).first()
        return user.to_dict()
    except:
        return None

def check_email_exists(email):
    user = User.query.filter_by(email=email).first()
    if user:
        return True
    return False

# filter user by email
def get_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    if user:
        return user.to_dict()
    return None

def check_phone_exists(uphone):
    #exists = lambda phone: User.query.filter_by(phone=phone).first() is not None
    #return exists
    user = User.query.filter_by(phone=uphone).first()
    if user:
        return True
    return False

# update a User
def update_user(db, firstname, lastname, email, country,
        country_code, phone, password, two_factor_auth_secret, 
        USER_ID):
    # get the user
    user = User.query.get(USER_ID)

    # update the user if it exists
    if user:
        user.email = email
        user.firstname = firstname
        user.lastname = lastname
        user.country = country
        user.country_code = country_code
        user.phone = phone
        user.password = password
        user.two_factor_auth_secret = two_factor_auth_secret
        user.date_updated = datetime.now()   
        # commit the changes
        db.session.commit()
        return user.to_dict()
    else:
        return None


# update a User
def update_user_status(db,  USER_ID, status):
    # get the user
    try:
        user = User.query.get(USER_ID)

        # update the user if it exists
        if user:
            user.status = status        
            user.date_updated = datetime.now()   
            # commit the changes
            db.session.commit()
            return user.to_dict()
        else:
            return None
    except Exception as e:
        return None

# delete a User
def delete_user(db, id):
    # get the user
    user = User.query.get(id)
    # delete the user if it exists
    if user:
        # delete the user
        db.session.delete(user)
        # commit the changes
        db.session.commit()
        # return the deleted user
        return user.to_dict()
    else:
        return None

