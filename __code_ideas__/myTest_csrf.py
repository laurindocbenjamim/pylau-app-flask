from flask import Flask, render_template, request, make_response
import secrets

"""
Basically for each request that modifies content on the server you would have to 
either use a one-time token and store that in the cookie and also transmit 
it with the form data. After receiving the data on the server again, you would 
then have to compare the two tokens and ensure they are equal.
"""

app = Flask(__name__)

# Generate a random CSRF token
def generate_csrf_token():
    return secrets.token_hex(16)

# Store the CSRF token in a cookie
def set_csrf_cookie(response):
    csrf_token = generate_csrf_token()
    response.set_cookie('csrf_token', csrf_token)
    return response

# Verify the CSRF token
def verify_csrf_token():
    csrf_token = request.cookies.get('csrf_token')
    if not csrf_token or csrf_token != request.form.get('csrf_token'):
        return False
    return True

# Route for the form submission
@app.route('/submit', methods=['POST'])
def submit_form():
    if not verify_csrf_token():
        return 'CSRF token verification failed', 403

    # Process the form data
    # ...

    return 'Form submitted successfully'

# Route for rendering the form
@app.route('/')
def render_form():
    response = make_response(render_template('form.html'))
    return set_csrf_cookie(response)

if __name__ == '__main__':
    app.run()