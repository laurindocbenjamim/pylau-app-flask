from flask import Flask, render_template, request, make_response
import secrets


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