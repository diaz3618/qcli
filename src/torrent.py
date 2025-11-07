
def torrent_status(session, host):
    """Fetch and log server status, free space, and active downloads."""
    try:
        resp = session.get(f"{host}/api/v2/sync/maindata")
        resp.raise_for_status()
        data = resp.json()
        free_space = data.get('server_state', {}).get('free_space_on_disk')
        dl_info = data.get('server_state', {}).get('dl_info_data')
        up_info = data.get('server_state', {}).get('up_info_data')
        active = sum(1 for t in data.get('torrents', {}).values() if t.get('state') == 'downloading')

        return {
            "free_space": free_space,
            "download_speed": dl_info,
            "upload_speed": up_info,
            "active_downloads": active
        }
    except Exception as e:
        raise

def torrent_move(session, host, hashes, path=None, category=None):
    """Move torrents to a new save path or category."""
    if path:
        resp = session.post(f"{host}/api/v2/torrents/setLocation", data={"hashes": hashes, "location": path})
        if resp.status_code != 200:
            raise Exception(f"Failed to move torrents: {resp.text}")
    if category:
        resp = session.post(f"{host}/api/v2/torrents/setCategory", data={"hashes": hashes, "category": category})
        if resp.status_code != 200:
            raise Exception(f"Failed to set category: {resp.text}")


def torrent_details(session, host, hash_):
    """Fetch and log details for a specific torrent."""
    try:
        resp = session.get(f"{host}/api/v2/torrents/properties", params={"hash": hash_})
        resp.raise_for_status()
        props = resp.json()

        return props
    except Exception as e:
        raise

def torrent_list(session, host, filter_mode="All"):
    """
    List all torrents, optionally filtered by status.
    filter_mode: One of All, Active, Downloading, Seeding, Completed, Stopped, Stalled, Errored
    Returns a list of dicts: [{hash, name, state}]
    """
    status_map = {
        "All": None,
        "Active": ["downloading", "uploading", "stalledUP", "stalledDL"],
        "Downloading": ["downloading", "stalledDL"],
        "Seeding": ["uploading", "stalledUP"],
        "Completed": ["completed"],
        "Stopped": ["pausedDL", "pausedUP"],
        "Stalled": ["stalledDL", "stalledUP"],
        "Errored": ["error"]
    }
    try:
        resp = session.get(f"{host}/api/v2/sync/maindata")
        resp.raise_for_status()
        torrents = resp.json().get("torrents", {})
        result = []
        for hash_, t in torrents.items():
            state = t.get("state", "")
            name = t.get("name", "")
            if filter_mode == "All" or (status_map[filter_mode] and state in status_map[filter_mode]):
                result.append({"hash": hash_, "name": name, "state": state})
        return result
    except Exception as e:
        raise
