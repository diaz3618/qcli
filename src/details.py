import logging
def show_details(session, host, hash_):
    try:
        resp = session.get(f"{host}/api/v2/torrents/properties", params={"hash": hash_})
        resp.raise_for_status()
        props = resp.json()
        for k, v in props.items():
            logging.info(f"{k}: {v}")
        return props
    except Exception as e:
        logging.error(f"Error fetching details for {hash_}: {e}")
        raise
