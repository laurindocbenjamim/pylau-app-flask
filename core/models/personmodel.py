
from sqlalchemy.orm import Mapped,mapped_column, relationship
from flask import jsonify
from core import db

class Person(db.Model):
    __tablename__ = 'person'
    personID:Mapped[int] = db.Column(db.Integer, primary_key=True, nullable=False)
    firstname:Mapped[str] = db.Column(db.String(100), nullable=False)
    lastname:Mapped[str] = db.Column(db.String(100), nullable=False)
    age:Mapped[int] = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Person {self.firstname} {self.lastname} with Age {self.age}>'
    
    def to_dict(self):
        return {
            'personID': self.personID,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'age': self.age
        }
    
