
from core import User

# create a person
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
    #pers = db.session.execute(db.select(Person).order_by(Person.firstname)).scalars()
    """person = Person.query.filter_by(personID=id).first()
    user = db.get_or_404(Person, id)
    return person.to_dict()"""

# update a person
def update_user(db, firstname, lastname, age):
    """person = Person(firstname=firstname, lastname=lastname, age=age)
    db.session.merge(person)
    db.session.commit()
    return person"""
