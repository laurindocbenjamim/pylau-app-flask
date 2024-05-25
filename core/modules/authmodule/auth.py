
import os
from flask import (
    Blueprint, render_template, url_for
)

bpapp = Blueprint("Auth", __name__, url_prefix='/auth')

@bpapp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('auth/auth.html')

@bpapp.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('auth/register.html')