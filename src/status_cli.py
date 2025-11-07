def print_status(session, host):
    def human_readable_size(num, suffix='B'):
        for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
            if abs(num) < 1024.0:
                return f"{num:3.1f} {unit}{suffix}"
            num /= 1024.0
        return f"{num:.1f} Y{suffix}"
    try:
        resp = session.get(f"{host}/api/v2/sync/maindata")
        resp.raise_for_status()
        data = resp.json()
        free_space = data.get('server_state', {}).get('free_space_on_disk')
        dl_info = data.get('server_state', {}).get('dl_info_data')
        up_info = data.get('server_state', {}).get('up_info_data')
        active = sum(1 for t in data.get('torrents', {}).values() if t.get('state') == 'downloading')
        print(f"Free space: {human_readable_size(free_space)}")
        print(f"Download speed: {human_readable_size(dl_info)}/s")
        print(f"Upload speed: {human_readable_size(up_info)}/s")
        print(f"Active downloads: {active}")
    except Exception as e:
        print(f"Error fetching server status: {e}")
        exit(1)
