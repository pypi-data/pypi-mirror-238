# master-auth

check auth use mongodb 

<!-- insert useage -->
## how to use

### install
```python
pip install master_auth
```

### example
```python
from master_auth import core
import os
import dotenv
dotenv.load_dotenv()

MONGODB_USER = os.getenv("MONGODB_USER")
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
MONGODB_HOST = os.getenv("MONGODB_HOST")
MONGODB_PORT = os.getenv("MONGODB_PORT")
DATABASE_NAME =  os.getenv("APP_NAME") + os.getenv("MONGODB_DATABASE_NAME")
COLLECTION_NAME = "master_auth"

def save_password(username,password):
    result = core.save_password(
        mongodb_username=MONGODB_USER,
        mongodb_password=MONGODB_PASSWORD,
        mongodb_host=MONGODB_HOST,
        mongodb_port=MONGODB_PORT,
        database_name = DATABASE_NAME,
        collection_name = COLLECTION_NAME,
        username = username,
        password = password
    )

    if result:
        print("Password saved successfully!")
        return True
    else:
        print("Username already exists!")
        return False

def update_password(username,password_old,password_new):
    result = core.update_password(
        mongodb_username=MONGODB_USER,
        mongodb_password=MONGODB_PASSWORD,
        mongodb_host=MONGODB_HOST,
        mongodb_port=MONGODB_PORT,
        database_name = DATABASE_NAME,
        collection_name = COLLECTION_NAME,
        username = username,
        password_old = password_old,
        password_new = password_new
    )

    if result:
        print("Password updated successfully!")
        return True
    else:
        print("Old password is not correct!")
        return False

def verify_password(username,password):
    result = core.verify_password(
        mongodb_username=MONGODB_USER,
        mongodb_password=MONGODB_PASSWORD,
        mongodb_host=MONGODB_HOST,
        mongodb_port=MONGODB_PORT,
        database_name = DATABASE_NAME,
        collection_name = COLLECTION_NAME,
        username = username,
        password = password
    )

   if result:
        print("Password is correct!")
        return True
   else:
        print("Password is not correct!")
        return False

if __name__ == "__main__":
    save_password("test","test")
    # Username does not exist!
    # Password saved successfully!

    # update_password("test","test","test2")
    # Password updated successfully!

    # verify_password("test","test2")
    # Password is correct!
```

## v0.0.2
- [x] update some bugs

## v0.0.1
- [x] save password to mongodb , password is hashed
- [x] check password from mongodb , password is hashed
- [x] update password to mongodb , password is hashed