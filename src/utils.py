import requests

def get_authenticated_session(args):
    host = getattr(args, 'host', "http://172.16.0.20:8080")
    user = getattr(args, 'user', "admin")
    password = getattr(args, 'password', "adminadmin")
    session = requests.Session()
    resp = session.post(f"{host}/api/v2/auth/login", data={"username": user, "password": password})
    if resp.text != "Ok.":
        raise Exception(f"Login failed: {resp.text}")
    return session
