import logging
def show_status(session, host):
    try:
        resp = session.get(f"{host}/api/v2/sync/maindata")
        resp.raise_for_status()
        data = resp.json()
        free_space = data.get('server_state', {}).get('free_space_on_disk')
        dl_info = data.get('server_state', {}).get('dl_info_data')
        up_info = data.get('server_state', {}).get('up_info_data')
        active = sum(1 for t in data.get('torrents', {}).values() if t.get('state') == 'downloading')
        logging.info(f"Free space: {free_space} bytes")
        logging.info(f"Download speed: {dl_info} bytes/s")
        logging.info(f"Upload speed: {up_info} bytes/s")
        logging.info(f"Active downloads: {active}")
        return {
            "free_space": free_space,
            "download_speed": dl_info,
            "upload_speed": up_info,
            "active_downloads": active
        }
    except Exception as e:
        logging.error(f"Error fetching server status: {e}")
        raise
