
import os
import psycopg2
from flask import url_for, session

PWD = 'ab6e8ad51efac658eca5c1b66056b9438d8866a522daeb3fee983b66970c0883'
USER='fiysuzvofhprpp'
DB = 'db5veivij96r5u'
PORT = '5432'
HOST = 'ec2-52-31-2-97.eu-west-1.compute.amazonaws.com'

DATABASE_URL = "jdbc:postgresql://ec2-52-31-2-97.eu-west-1.compute.amazonaws.com:5432/db5veivij96r5u?sslmode=require&user=fiysuzvofhprpp&password=ab6e8ad51efac658eca5c1b66056b9438d8866a522daeb3fee983b66970c0883"
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

