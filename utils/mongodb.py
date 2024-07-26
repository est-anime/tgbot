from pymongo import MongoClient
from config import MONGODB_URI, DATABASE_NAME

client = MongoClient(MONGODB_URI)
db = client[DATABASE_NAME]

def get_users_collection():
    return db['users']

def get_banned_users_collection():
    return db['banned_users']

def add_user(user_id, username):
    users = get_users_collection()
    if users.find_one({'user_id': user_id}) is None:
        users.insert_one({'user_id': user_id, 'username': username})

def get_all_users():
    users = get_users_collection()
    return list(users.find({}, {'_id': 0, 'user_id': 1, 'username': 1}))

def add_banned_user(user_id):
    banned_users = get_banned_users_collection()
    if banned_users.find_one({'user_id': user_id}) is None:
        banned_users.insert_one({'user_id': user_id})

def remove_banned_user(user_id):
    banned_users = get_banned_users_collection()
    banned_users.delete_one({'user_id': user_id})

def is_banned(user_id):
    banned_users = get_banned_users_collection()
    return banned_users.find_one({'user_id': user_id}) is not None
