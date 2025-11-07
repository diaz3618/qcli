def move_torrents_cli(session, host, hashes, path=None, category=None):
    if path:
        resp = session.post(f"{host}/api/v2/torrents/setLocation", data={"hashes": hashes, "location": path})
        if resp.status_code == 200:
            print(f"Moved torrents to {path}")
        else:
            print(f"Failed to move torrents: {resp.text}")
            exit(1)
    if category:
        resp = session.post(f"{host}/api/v2/torrents/setCategory", data={"hashes": hashes, "category": category})
        if resp.status_code == 200:
            print(f"Set category to {category}")
        else:
            print(f"Failed to set category: {resp.text}")
            exit(1)
