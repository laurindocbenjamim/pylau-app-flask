from flask import Flask, redirect, request

"""
HTTP Strict Transport Security (HSTS)¶
Tells the browser to convert all HTTP requests to HTTPS, preventing man-in-the-middle (MITM) attacks.
"""
"""app = Flask(__name__)

# Enable HSTS for all routes
@app.before_request
def enforce_https():
    if not request.is_secure:
        return redirect(request.url.replace('http://', 'https://'), code=301)

# Your routes go here
@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'This is the about page.'

if __name__ == '__main__':
    app.run(ssl_context='adhoc')
"""

app = Flask(__name__)

# Enable HSTS for all routes
@app.before_request
def enforce_https():
    if not request.is_secure:
        return redirect(request.url.replace('http://', 'https://'), code=301)

# Your routes go here
@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'This is the about page.'

if __name__ == '__main__':
    app.run(ssl_context='adhoc')

