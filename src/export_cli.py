from datetime import datetime
import os

def export_torrents_cli(session, host, export_dir, category=None, tag=None, state=None):
    os.makedirs(export_dir, exist_ok=True)
    log_path = os.path.join(export_dir, "export_errors.log")
    def log_error(msg):
        with open(log_path, "a") as logf:
            logf.write(msg + "\n")
    filter_params = {}
    if category:
        filter_params['category'] = category
    if tag:
        filter_params['tag'] = tag
    if state:
        filter_params['filter'] = state
    try:
        resp = session.get(f"{host}/api/v2/torrents/info", params=filter_params)
        resp.raise_for_status()
        torrents = resp.json()
        if not torrents:
            print("No torrents found for the given filters.")
            exit(2)
    except Exception as e:
        print(f"Error fetching torrent list: {e}")
        log_error(f"Error fetching torrent list: {e}")
        exit(1)
    dt_str = datetime.now().strftime("%Y%m%d-%H%M")
    magnets_path = os.path.join(export_dir, f"{dt_str}_magnets.txt")
    with open(magnets_path, "w") as mf:
        for t in torrents:
            name = t.get('name')
            hash_ = t.get('hash')
            magnet = t.get('magnet_uri') if 'magnet_uri' in t else None
            if not magnet:
                trackers = t.get('trackers', [])
                dn = name.replace(' ', '+') if name else hash_
                magnet = f"magnet:?xt=urn:btih:{hash_}&dn={dn}"
                for tr in trackers:
                    magnet += f"&tr={tr}"
            if magnet:
                mf.write(magnet + "\n")
    print(f"All magnet links exported to: {magnets_path}")
