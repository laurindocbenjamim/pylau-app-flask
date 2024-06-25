
import os
import psycopg2
from flask import url_for, session

PWD = ''
USER=''
DB = ''
PORT = ''
HOST = ''

DATABASE_URL = "jdbc:postgresql://{HOST}:{PORT}/{DB}?sslmode=require&user={USER}&password={PWD}".format(HOST=HOST,PORT=PORT,DB=DB,USER=USER,PWD=PWD)
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

print(conn)

from werkzeug.security import check_password_hash, generate_password_hash
# Encrypt password
def encrypt_password(password):
    return generate_password_hash(password)

# Decrypt password
def decrypt_password(encrypted_password, password):
    return check_password_hash(encrypted_password, password)

password = 'admin'
#pwd = encrypt_password(password)
#print(pwd)

#print(decrypt_password(pwd, 'password'))

print(DATABASE_URL)

