
from classes import User
import sqlite3

def user_adapter(user):
    print("user adapter called")
    return f"{user.name};{user.uid}"
def user_converter(bytestring):
    print("user converter called")
    username, uid = bytestring.split(b";")
    return User(str(username), int(uid))
    
sqlite3.register_adapter(User, user_adapter)
sqlite3.register_converter("USER", user_converter)