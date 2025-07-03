# auth functions
# Not used now — but can be extended for real login systems
users = {
    "admin": "admin"
}

def check_login(username, password):
    return users.get(username) == password
