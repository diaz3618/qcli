#!/usr/bin/env python3
import argparse
import os
import sys
from src.color import color_state
from src.add import add_magnet_cli, add_torrent_cli, add_magnet_file_cli
from src.utils import get_authenticated_session
from src.status_cli import print_status
from src.move_cli import move_torrents_cli
from src.details_cli import show_details_cli
from src.export_cli import export_torrents_cli
from src.importer_cli import import_torrents_cli
from src.compare_cli import compare_torrents_cli
from src.torrent import torrent_list
from src.listing import print_torrent_table

def main():
    parser = argparse.ArgumentParser(description="qcli: Send magnet or .torrent to qBittorrent server, and much more.")
    DEFAULT_HOST = "http://172.16.0.20:8080"
    DEFAULT_USER = "admin"
    DEFAULT_PASS = "adminadmin"

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--magnet", help="Magnet link to add")
    group.add_argument("--torrent", help="Path to .torrent file to add")
    group.add_argument("--magnet-file", help="Path to file with magnet links (one per line)")
    group.add_argument("--status", action="store_true", help="Show server health, free space, and active downloads")
    group.add_argument("--move", nargs=1, metavar="HASHES", help="Move torrents to new save path or category (comma separated hashes)")
    group.add_argument("--details", metavar="HASH", help="Show full info for a specific torrent by hash")
    group.add_argument("--export", metavar="DIR", help="Export all torrents to directory")
    group.add_argument("--import-dir", metavar="DIR", help="Import all .torrent files from directory")
    group.add_argument("--compare", nargs=3, metavar=("HOST1", "USER1", "PASS1"), help="Compare torrents between two servers")
    group.add_argument("--list-torrents", nargs="?", metavar="FILTER", default=None, help="List torrents (optionally filter: All, Active, Downloading, Seeding, Completed, Stopped, Stalled, Errored)")
    parser.add_argument("--path", required=False, help="Download save path on server")
    parser.add_argument("--host", default=DEFAULT_HOST, help="qBittorrent WebUI host URL")
    parser.add_argument("--user", default=DEFAULT_USER, help="qBittorrent WebUI username")
    parser.add_argument("--pass", dest="password", default=DEFAULT_PASS, help="qBittorrent WebUI password")
    parser.add_argument("--category", help="Category for move/export")
    parser.add_argument("--tag", help="Tag for export")
    parser.add_argument("--state", help="State filter for export")

    import contextlib
    import io
    sys_argv = sys.argv[1:]
    if not sys_argv:
        parser.print_help()
        sys.exit(0)
    with contextlib.redirect_stderr(io.StringIO()):
        try:
            args = parser.parse_args()
        except SystemExit as e:
            parser.print_help()
            sys.exit(0)

    try:
        session = get_authenticated_session(args)
    except Exception as e:
        print(f"Login failed: {e}")
        sys.exit(1)

    if args.list_torrents is not None:
        filter_mode = args.list_torrents if args.list_torrents else "All"
        try:
            torrents = torrent_list(session, args.host, filter_mode)
        except Exception as e:
            print(f"Error listing torrents: {e}")
            sys.exit(0)
        print_torrent_table(torrents, filter_mode)
        sys.exit(0)

    if args.magnet:
        add_magnet_cli(session, args.host, args.magnet, args.path)
    elif args.torrent:
        add_torrent_cli(session, args.host, args.torrent, args.path)
    elif args.magnet_file:
        add_magnet_file_cli(session, args.host, args.magnet_file, args.path)
    elif args.status:
        print_status(session, args.host)
    elif args.move:
        hashes = args.move[0]
        move_torrents_cli(session, args.host, hashes, path=args.path, category=args.category)
    elif args.details:
        show_details_cli(session, args.host, args.details)
    elif args.export:
        export_torrents_cli(
            session,
            args.host,
            args.export,
            category=args.category,
            tag=args.tag,
            state=args.state
        )
    elif args.import_dir:
        import_torrents_cli(session, args.host, args.import_dir)
    elif args.compare:
        host, user, password = args.compare
        compare_torrents_cli(
            session,
            host, user, password,
            args.host, args.user, args.password
        )

if __name__ == "__main__":
    main()
