import logging
def move_torrents(session, host, hashes, path=None, category=None):
    if path:
        resp = session.post(f"{host}/api/v2/torrents/setLocation", data={"hashes": hashes, "location": path})
        if resp.status_code == 200:
            logging.info(f"Moved torrents to {path}")
        else:
            logging.error(f"Failed to move torrents: {resp.text}")
            raise Exception(f"Failed to move torrents: {resp.text}")
    if category:
        resp = session.post(f"{host}/api/v2/torrents/setCategory", data={"hashes": hashes, "category": category})
        if resp.status_code == 200:
            logging.info(f"Set category to {category}")
        else:
            logging.error(f"Failed to set category: {resp.text}")
            raise Exception(f"Failed to set category: {resp.text}")
