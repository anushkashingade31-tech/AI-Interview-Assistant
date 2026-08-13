import bcrypt

def hash_password(password):
    password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password, salt)

def verify_password(password, hashed_password):
    password = password.encode('utf-8')
    return bcrypt.checkpw(password, hashed_password.encode('utf-8'))