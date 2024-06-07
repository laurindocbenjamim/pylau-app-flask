
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User():

    __tablename__ = 'users'

    def __repr__(self) -> str:
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    
    def list_users():
        return [
            {   'id': 1,
                'username': 'admin',
                'name': 'Mauro Aragao',
                'email': 'admin@email.com'
            },
            {   'id': 2,
                'username': 'aurora',
                'name': 'Aurora Camacho',
                'email': 'aurora@email.com'
            },
        ]
    