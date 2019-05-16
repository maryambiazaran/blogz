import hashlib
import os
import base64

def make_salt():
    b_salt = os.urandom(6)
    return base64.b64encode(b_salt).decode()

def make_pw_hash(password, salt=None):
    if salt is None:
        salt = make_salt()
    my_hash = hashlib.sha256()
    my_hash.update(str.encode(password))
    my_hash.update(str.encode(salt))
    return '{}:{}'.format(my_hash.hexdigest(),salt)

def check_pw_hash(password, stored_hash):
    salt = stored_hash.split(':')[1]
    hashed_password = make_pw_hash(password, salt)
    return hashed_password == stored_hash
