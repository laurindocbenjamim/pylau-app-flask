from flask import Flask, make_response, session, jsonify

app = Flask(__name__)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = 600


@app.route('/')
def index():
    response = make_response('Hello, world!')
    # cookie expires after 10 minutes
    response.set_cookie('my_cookie', 'cookie_value', secure=True, httponly=True, samesite='Lax', max_age=600)

    
    return response


@app.route('/login', methods=['POST'])
def login():
    session.clear()
    session['user_id'] = 1
    """
    For the session cookie, if session.permanent is set, then PERMANENT_SESSION_LIFETIME 
    is used to set the expiration. Flask’s default cookie implementation validates that the cryptographic signature 
    is not older than this value. Lowering this value may help mitigate replay attacks,
     where intercepted cookies can be sent at a later time.
    """
    session.permanent = True
    return jsonify({'message': 'User logged in'})

if __name__ == '__main__':
    app.run()




    