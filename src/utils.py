import requests


def get_authenticated_session(host, user, password):
    session = requests.Session()
    resp = session.post(f"{host}/api/v2/auth/login", data={"username": user, "password": password})
    if resp.text != "Ok.":
        raise Exception(f"Login failed: {resp.text}")
    return session
