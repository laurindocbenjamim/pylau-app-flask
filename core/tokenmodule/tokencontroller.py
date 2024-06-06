
# Import the Token class from the core module
from core import Token

"""
The provided code defines a function called create_token that takes three 
parameters: userID, token, and expire_time. This function is responsible for creating a 
new token and storing it in a database.

Inside the function, a new instance of the Token class is created using the provided 
userID, token, and expire_time values. This new token is assigned to the variable new_token.

Next, the new_token object is added to the database session using the db.session.add() method. 
This method adds the object to the session, preparing it to be committed to the database.

Finally, the changes made to the session are committed using the db.session.commit() method. 
This ensures that the new token is permanently stored in the database.

The function then returns the new_token object, allowing the caller to access the created token if needed.

It's important to note that this code assumes the existence of a Token class and a db 
object that provides access to the database session. Additionally, the code relies on an external library or 
framework that provides the db.session functionality.


"""
# Create a new token
def create_token(db,userID, token, expire_time):
    new_token = Token(userID=userID, token=token, expire_time=expire_time)
    db.session.add(new_token)
    db.session.commit()
    return new_token.to_dict()
    

# Get a token by its ID
def get_token_by_id(tokenID):
    try:
        return [token.to_dict() for token in Token.query.filter_by(tokenID=tokenID).all()]
    except Exception as e:
        return None
    
# Get a token by its token
def get_token_by_token(token):
    try:
        return [token.to_dict() for token in Token.query.filter_by(token=token).all()]
    except Exception as e:
        return None
    
# Delete a token by its ID
def delete_token(db,tokenID):
    try:
        Token.query.filter_by(tokenID=tokenID).delete()
        db.session.commit()
        return True
    except Exception as e:
        return False
    