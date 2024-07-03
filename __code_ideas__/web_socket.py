"""
In the provided code, the web socket functionality is implemented using the Flask-SocketIO library. The web socket allows for real-time,
 bidirectional communication between the client (web browser) and the server.

The socketio object is an instance of the SocketIO class, which is responsible for handling the web socket connections. It is initialized with the Flask application (app) as its argument.

The @socketio.on('connect') decorator is used to define a function that will be executed when a client connects to the server via a web socket. In this case, the handle_connect() function is called, which simply prints a message indicating that a client has connected.

Similarly, the @socketio.on('disconnect') decorator is used to define a function that will be executed when a client disconnects from the server. The handle_disconnect() function is called in this case, which prints a message indicating that a client has disconnected.

The @socketio.on('message') decorator is used to define a function that will be executed when the server receives a message from a client. The handle_message(data) function is called, which prints the received message and emits a response back to the client using the emit() function.

Overall, the web socket functionality allows the server to receive messages from clients and send responses back in real-time, enabling interactive and dynamic communication between the client and the server.


"""

import os
from flask import Flask, render_template
#pip install flask-socketio
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('message')
def handle_message(data):
    print('Received message:', data)
    emit('response', 'Server received your message')

if __name__ == '__main__':
    socketio.run(app)