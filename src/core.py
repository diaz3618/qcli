import sys
import requests

def login(session, host, username, password):
    resp = session.post(f"{host}/api/v2/auth/login", data={"username": username, "password": password})
    if resp.text != "Ok.":
        print("Login failed:", resp.text)
        sys.exit(1)

def add_magnet(session, host, magnet, savepath):
    resp = session.post(f"{host}/api/v2/torrents/add", data={"urls": magnet, "savepath": savepath})
    if resp.status_code != 200:
        print("Failed to add magnet link:", resp.text)
        sys.exit(1)
    info = session.get(f"{host}/api/v2/torrents/info", params={"filter": "all", "limit": 1, "sort": "added_on", "reverse": "true"})
    import datetime
    def color(text, code):
        return f"\033[{code}m{text}\033[0m"
    if info.status_code == 200 and info.json():
        torrent = info.json()[0]
        name = color(torrent.get('name', ''), '34')
        hash_ = color(torrent.get('hash', ''), '33')
        added = torrent.get('added_on')
        if added:
            added_str = datetime.datetime.fromtimestamp(added).strftime('%Y-%m-%d %H:%M:%S')
            added_str = color(added_str, '36')
        else:
            added_str = ''
        print(f"\n{color('✔ Magnet link added successfully!', '32')}\n  {color('Name:', '1;34')} {name}\n  {color('Hash:', '1;33')} {hash_}\n  {color('Added:', '1;36')} {added_str}")
    else:
        print("\n" + color("Magnet link added, but could not confirm from server.", '32'))

def add_torrent(session, host, torrent_path, savepath):
    with open(torrent_path, "rb") as f:
        files = {"torrents": f}
        data = {"savepath": savepath}
        resp = session.post(f"{host}/api/v2/torrents/add", files=files, data=data)
    if resp.status_code != 200:
        print("Failed to add torrent file:", resp.text)
        sys.exit(1)
    info = session.get(f"{host}/api/v2/torrents/info", params={"filter": "all", "limit": 1, "sort": "added_on", "reverse": "true"})
    import datetime
    def color(text, code):
        return f"\033[{code}m{text}\033[0m"
    if info.status_code == 200 and info.json():
        torrent = info.json()[0]
        name = color(torrent.get('name', ''), '34')
        hash_ = color(torrent.get('hash', ''), '33')
        added = torrent.get('added_on')
        if added:
            added_str = datetime.datetime.fromtimestamp(added).strftime('%Y-%m-%d %H:%M:%S')
            added_str = color(added_str, '36')
        else:
            added_str = ''
        print(f"\n{color('✔ Torrent file added successfully!', '32')}\n  {color('Name:', '1;34')} {name}\n  {color('Hash:', '1;33')} {hash_}\n  {color('Added:', '1;36')} {added_str}")
    else:
        print("\n" + color("Torrent file added, but could not confirm from server.", '32'))
