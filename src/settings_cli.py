"""
settings_cli.py
CLI for viewing and changing qBittorrent WebUI settings.
"""
import argparse
import requests
import sys


from src.utils import get_authenticated_session

def list_settings(host, session):
    resp = session.get(f"{host}/api/v2/app/preferences")
    if resp.status_code != 200:
        print("Failed to fetch settings.", file=sys.stderr)
        sys.exit(1)
    prefs = resp.json()
    for k, v in prefs.items():
        print(f"{k}: {v}")

def set_setting(host, session, key, value):
    resp = session.post(f"{host}/api/v2/app/setPreferences", json={key: value})
    if resp.status_code != 200:
        print("Failed to set setting.", file=sys.stderr)
        sys.exit(1)
    print(f"Set {key} to {value}")

def main():
    parser = argparse.ArgumentParser(description="View or change qBittorrent WebUI settings")
    parser.add_argument("--host", required=True, help="qBittorrent WebUI host, e.g. http://localhost:8080")
    parser.add_argument("--user", required=True, help="WebUI username")
    parser.add_argument("--pass", required=True, dest="password", help="WebUI password")
    subparsers = parser.add_subparsers(dest="command")

    list_parser = subparsers.add_parser("list", help="List all settings")
    set_parser = subparsers.add_parser("set", help="Set a setting")
    set_parser.add_argument("key", help="Setting key")
    set_parser.add_argument("value", help="New value")

    args = parser.parse_args()
    session = get_authenticated_session(args.host, args.user, args.password)

    if args.command == "list":
        list_settings(args.host, session)
    elif args.command == "set":
        set_setting(args.host, session, args.key, args.value)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
