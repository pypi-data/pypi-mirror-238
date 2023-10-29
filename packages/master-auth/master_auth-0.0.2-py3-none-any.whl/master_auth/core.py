import pymongo
import bcrypt


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def save_password(mongodb_username, mongodb_password, mongodb_host, mongodb_port, database_name, collection_name, username, password):
    client = pymongo.MongoClient(f"mongodb://{mongodb_username}:{mongodb_password}@{mongodb_host}:{mongodb_port}/?authMechanism=DEFAULT")
    db = client[database_name]
    collection = db[collection_name]
    
    # check username exist or not
    user = collection.find_one({"username": username})
    if user:
        print("Username already exists!")
        return False
    else:
        print("Username does not exist!")
        result = collection.insert_one({"username": username, "password": hash_password(password)})

        if result.acknowledged:
            print("Password saved successfully!")
            return True
        else:
            print("Password not saved!")
            return False
        
def verify_password(mongodb_username, mongodb_password, mongodb_host, mongodb_port, database_name, collection_name, username, password):
    client = pymongo.MongoClient(f"mongodb://{mongodb_username}:{mongodb_password}@{mongodb_host}:{mongodb_port}/?authMechanism=DEFAULT")
    db = client[database_name]
    collection = db[collection_name]
    user = collection.find_one({"username": username})
    
    if user:
        hashed_password = user["password"]
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            print("Password is correct!")
            return True
        else:
            print("Password is not correct!")
            return False
    else:
        print("Username does not exist!")
        return False

def update_password(mongodb_username, mongodb_password, mongodb_host, mongodb_port, database_name, collection_name, username, password_old, password_new):
    client = pymongo.MongoClient(f"mongodb://{mongodb_username}:{mongodb_password}@{mongodb_host}:{mongodb_port}/?authMechanism=DEFAULT")
    db = client[database_name]
    collection = db[collection_name]
    user = collection.find_one({"username": username})
    
    if user:
        # check old password is correct or not
        hashed_password = user["password"]
        if bcrypt.checkpw(password_old.encode('utf-8'), hashed_password.encode('utf-8')):
            result = collection.update_one({"username": username}, {"$set": {"password": hash_password(password_new)}})
            if result.acknowledged:
                print("Password updated successfully!")
                return True
            else:
                print("Password not updated!")
                return False
        else:
            print("Old password is not correct!")
            return False
    else:
        print("Username does not exist!")
        return False


