def show_details_cli(session, host, hash_):
    try:
        resp = session.get(f"{host}/api/v2/torrents/properties", params={"hash": hash_})
        resp.raise_for_status()
        props = resp.json()
        for k, v in props.items():
            print(f"{k}: {v}")
    except Exception as e:
        print(f"Error fetching details for {hash_}: {e}")
        exit(1)
