
from core.models.personmodel import Person

# create a person
def create_person(db, firstname, lastname, age):
    object = Person(firstname=firstname, lastname=lastname, age=age)
    db.session.add(object)
    db.session.commit()
    return object

# select all people
def get_all_people(db):
    #people = db.session.query(Person).all()
    objects = [person.to_dict() for person in Person.query.all()]

    return objects

# filter people by id
def get_person_by_id(db,id):
    #pers = db.session.execute(db.select(Person).order_by(Person.firstname)).scalars()
    object = Person.query.filter_by(personID=id).first()
    user = db.get_or_404(Person, id)
    return object.to_dict()

# update a person
def update_person(db, firstname, lastname, age):
    object = Person(firstname=firstname, lastname=lastname, age=age)
    db.session.merge(object)
    db.session.commit()
    return object
