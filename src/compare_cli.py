from src.utils import get_authenticated_session

def compare_torrents_cli(session, host, user, password, src_host, src_user, src_password):
    def get_hashes(host, user, password):
        class Args:
            pass
        args_obj = Args()
        args_obj.host = host
        args_obj.user = user
        args_obj.password = password
        try:
            s = get_authenticated_session(args_obj)
            resp = s.get(f"{host}/api/v2/torrents/info")
            resp.raise_for_status()
            return set(t['hash'] for t in resp.json())
        except Exception as e:
            print(f"Error fetching hashes from {host}: {e}")
            return set()
    src_hashes = get_hashes(src_host, src_user, src_password)
    cmp_hashes = get_hashes(host, user, password)
    if not src_hashes or not cmp_hashes:
        print("Error: Could not fetch hashes from one or both servers.")
        exit(1)
    only_in_src = src_hashes - cmp_hashes
    only_in_cmp = cmp_hashes - src_hashes
    both = src_hashes & cmp_hashes
    print(f"Torrents only in source: {len(only_in_src)}")
    print(f"Torrents only in compare: {len(only_in_cmp)}")
    print(f"Torrents in both: {len(both)}")
