
from core import AuthUserRegisterModel

# create a User
def regist_user_auth(db, user_id, username, device, device_ip, device_mac):
    object = AuthUserRegisterModel(
        user_id = user_id,
        username = username,    
        device = device,
        device_ip = device_ip,
        device_mac = device_mac
    
        )
    db.session.add(object)
    db.session.commit()
    return object

# select all people
def get_user_auth_hists(db):
    #user = db.session.query(User).all()
    user = [user.to_dict() for user in AuthUserRegisterModel.query.all()]

    return user

# filter people by id
def get_user_auth_hist_by_id(db,id):
    #pers = db.session.execute(db.select(user).order_by(User.firstname)).scalars()
    user = AuthUserRegisterModel.query.filter_by(user_id=id).first()
    
    return user.to_dict()

# update a User
def update_auth_status(db, time_logout, id):
    user = AuthUserRegisterModel.query.get(id)
    if user:
        user.time_logout = time_logout
        db.session.commit()
        return user.to_dict()
    else:
        return None

# delete a User
def delete_user_auth_hist(db, id):
    user = AuthUserRegisterModel.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return user.to_dict()
    else:
        return None
