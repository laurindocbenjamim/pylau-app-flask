
from core import User
from datetime import datetime

# create a User
def create_user(db, firstname, lastname, email, country,
        country_code, phone, password, two_factor_auth_code):
    object = User( 
        firstname = firstname,
        lastname = lastname,
        email = email,
        country = country,
        country_code = country_code,
        phone = phone,
        password = password,
        two_factor_auth_code = two_factor_auth_code
    )
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

# update a User
def update_user(db, firstname, lastname, email, country,
        country_code, phone, password, two_factor_auth_code, 
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
        user.two_factor_auth_code = two_factor_auth_code
        user.date_updated = datetime.now()   
        # commit the changes
        db.session.commit()
        return user.to_dict()
    else:
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