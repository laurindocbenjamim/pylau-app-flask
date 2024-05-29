
from core.models.personmodel import Person

# create a person
def create_person(db, firstname, lastname, age):
    person = Person(firstname=firstname, lastname=lastname, age=age)
    db.session.add(person)
    db.session.commit()
    return person

# select all people
def get_all_people(db):
    #people = db.session.query(Person).all()
    people = [person.to_dict() for person in Person.query.all()]

    return people

# filter people by id
def get_person_by_id(db,id):
    #pers = db.session.execute(db.select(Person).order_by(Person.firstname)).scalars()
    person = Person.query.filter_by(personID=id).first()
    user = db.get_or_404(Person, id)
    return person.to_dict()

# update a person
def update_person(db, firstname, lastname, age):
    person = Person(firstname=firstname, lastname=lastname, age=age)
    db.session.merge(person)
    db.session.commit()
    return person
