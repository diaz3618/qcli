import os
from src.core import add_magnet, add_torrent

def add_magnet_cli(session, host, magnet, path):
    if not path:
        print("--path is required for magnet")
        exit(2)
    add_magnet(session, host, magnet, path)

def add_torrent_cli(session, host, torrent_path, path):
    if not path:
        print("--path is required for torrent")
        exit(2)
    if not os.path.isfile(torrent_path):
        print("Torrent file not found:", torrent_path)
        exit(1)
    add_torrent(session, host, torrent_path, path)

def add_magnet_file_cli(session, host, magnet_file, path):
    if not path:
        print("--path is required for magnet-file")
        exit(2)
    if not os.path.isfile(magnet_file):
        print("Magnet file not found:", magnet_file)
        exit(1)
    with open(magnet_file) as f:
        for line in f:
            magnet = line.strip()
            if magnet:
                print(f"Adding magnet: {magnet}")
                add_magnet(session, host, magnet, path)
