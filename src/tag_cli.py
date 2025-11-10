def manage_tags_cli(session, host, action, tag_name=None, torrent_hashes=None):
    """
    Manage qBittorrent tags
    """
    if action == "list":
        try:
            resp = session.get(f"{host}/api/v2/torrents/tags")
            resp.raise_for_status()
            tags = resp.json()
            
            if not tags:
                print("No tags found.")
                return
                
            print("Available tags:")
            for tag in sorted(tags):
                print(f"  - {tag}")
                
        except Exception as e:
            print(f"Error fetching tags: {e}")
            exit(1)
            
    elif action == "add":
        if not tag_name:
            print("Tag name is required for add operation")
            exit(1)
        if not torrent_hashes:
            print("Torrent hashes are required for add operation (use 'all' for all torrents)")
            exit(1)
            
        try:
            
            if torrent_hashes.lower() == "all":
                resp = session.get(f"{host}/api/v2/torrents/info")
                resp.raise_for_status()
                torrents = resp.json()
                torrent_hashes = "|".join([t['hash'] for t in torrents])
            else:
                
                torrent_hashes = torrent_hashes.replace(",", "|")
                
            data = {'hashes': torrent_hashes, 'tags': tag_name}
            resp = session.post(f"{host}/api/v2/torrents/addTags", data=data)
            resp.raise_for_status()
            
            if resp.status_code == 200:
                print(f"Tag '{tag_name}' added to specified torrents.")
            else:
                print(f"Failed to add tag: {resp.text}")
                exit(1)
                
        except Exception as e:
            print(f"Error adding tag: {e}")
            exit(1)
            
    elif action == "remove":
        if not tag_name:
            print("Tag name is required for remove operation")
            exit(1)
        if not torrent_hashes:
            print("Torrent hashes are required for remove operation (use 'all' for all torrents)")
            exit(1)
            
        try:
            
            if torrent_hashes.lower() == "all":
                resp = session.get(f"{host}/api/v2/torrents/info")
                resp.raise_for_status()
                torrents = resp.json()
                torrent_hashes = "|".join([t['hash'] for t in torrents])
            else:
                
                torrent_hashes = torrent_hashes.replace(",", "|")
                
            data = {'hashes': torrent_hashes, 'tags': tag_name}
            resp = session.post(f"{host}/api/v2/torrents/removeTags", data=data)
            resp.raise_for_status()
            
            if resp.status_code == 200:
                print(f"Tag '{tag_name}' removed from specified torrents.")
            else:
                print(f"Failed to remove tag: {resp.text}")
                exit(1)
                
        except Exception as e:
            print(f"Error removing tag: {e}")
            exit(1)
            
    elif action == "delete":
        if not tag_name:
            print("Tag name is required for delete operation")
            exit(1)
            
        try:
            
            resp = session.get(f"{host}/api/v2/torrents/info")
            resp.raise_for_status()
            torrents = resp.json()
            
            if torrents:
                all_hashes = "|".join([t['hash'] for t in torrents])
                data = {'hashes': all_hashes, 'tags': tag_name}
                resp = session.post(f"{host}/api/v2/torrents/removeTags", data=data)
                resp.raise_for_status()
            
            print(f"Tag '{tag_name}' deleted from all torrents.")
                
        except Exception as e:
            print(f"Error deleting tag: {e}")
            exit(1)
            
    else:
        print("Invalid action. Use: list, add, remove, or delete")
        exit(1)