# This file contains all the dependencies that are required for the application to run
import os
import secrets
import pyotp
import imghdr
import uuid
import string

# Importing the required libraries
from datetime import datetime
from datetime import timedelta
#from flask_wtf import CSRFProtect
from flask_wtf.csrf import CSRFProtect, generate_csrf, validate_csrf
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_caching import Cache
from flask import Flask, send_file
from flask import request
from flask import session
from flask import jsonify
from flask import json as flask_json
from flask import Blueprint
from flask import current_app
from quart import Quart
from quart import websocket
from flask import make_response
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
from markupsafe import escape
from flask import render_template
from flask import send_file
from flask import redirect
from flask import flash
from flask import abort
from flask import url_for
from flask_cors import CORS
from flask_cors import cross_origin
from flask_talisman import Talisman
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_restful import Api, Resource
from flask_limiter.util import get_remote_address
#Importing the mongoDB library
from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask import current_app