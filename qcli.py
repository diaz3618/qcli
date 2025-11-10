#!/usr/bin/env python3
import argparse
import os
import sys
import json
from src.color import color_state
from src.add import add_magnet_cli, add_torrent_cli, add_magnet_file_cli
from src.utils import get_authenticated_session
from src.status_cli import print_status
from src.move_cli import move_torrents_cli
from src.details_cli import show_details_cli
from src.export_cli import export_torrents_cli
from src.importer_cli import import_torrents_cli
from src.compare_cli import compare_torrents_cli
from src.category_cli import manage_categories_cli
from src.tag_cli import manage_tags_cli
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
    group.add_argument("--list-torrents", nargs="?", metavar="FILTER", const="All", default=None, help="List torrents (optionally filter: All, Active, Downloading, Seeding, Completed, Stopped, Stalled, Errored)")
    group.add_argument("--settings", nargs="*", metavar="ARGS", help="View or change WebUI settings. Usage: --settings list OR --settings set <key> <value>")
    group.add_argument("--manage-categories", nargs="*", metavar="ARGS", help="Manage categories. Usage: --manage-categories list | add <name> [save-path] | delete <name> | edit <name> <save-path>")
    group.add_argument("--manage-tags", nargs="*", metavar="ARGS", help="Manage tags. Usage: --manage-tags list | add <tag> <hashes> | remove <tag> <hashes> | delete <tag>")
    parser.add_argument("--path", required=False, help="Download save path on server")
    parser.add_argument("--host", default=DEFAULT_HOST, help="qBittorrent WebUI host URL")
    parser.add_argument("--user", default=DEFAULT_USER, help="qBittorrent WebUI username")
    parser.add_argument("--pass", dest="password", default=DEFAULT_PASS, help="qBittorrent WebUI password")
    parser.add_argument("--category", help="Category for move/export")
    parser.add_argument("--tag", help="Tag for export")
    parser.add_argument("--state", help="State filter for export")

    args = parser.parse_args()

    try:
        session = get_authenticated_session(args.host, args.user, args.password)
    except Exception as e:
        print(f"Login failed: {e}")
        sys.exit(1)

    if args.settings is not None:
        host = args.host
        user = args.user
        password = args.password
    
        categories = {
            "Behavior": [
                "locale", "performance_warning", "status_bar_external_ip", "confirm_torrent_deletion", "file_log_enabled", "file_log_path", "file_log_backup_enabled", "file_log_max_size", "file_log_delete_old", "file_log_age", "file_log_age_type", "delete_torrent_content_files"
            ],
            "Downloads": [
                "torrent_content_layout", "add_to_top_of_queue", "add_stopped_enabled", "torrent_stop_condition", "merge_trackers", "auto_delete_mode", "preallocate_all", "incomplete_files_ext", "use_unwanted_folder", "auto_tmm_enabled", "torrent_changed_tmm_enabled", "save_path_changed_tmm_enabled", "category_changed_tmm_enabled", "use_subcategories", "save_path", "temp_path_enabled", "temp_path", "use_category_paths_in_manual_mode", "export_dir", "export_dir_fin", "scan_dirs", "excluded_file_names_enabled", "excluded_file_names"
            ],
            "Notifications": [
                "mail_notification_enabled", "mail_notification_sender", "mail_notification_email", "mail_notification_smtp", "mail_notification_ssl_enabled", "mail_notification_auth_enabled", "mail_notification_username", "mail_notification_password", "autorun_on_torrent_added_enabled", "autorun_on_torrent_added_program", "autorun_enabled", "autorun_program"
            ],
            "Connection": [
                "listen_port", "ssl_enabled", "ssl_listen_port", "random_port", "upnp", "max_connec", "max_connec_per_torrent", "max_uploads", "max_uploads_per_torrent"
            ],
            "I2P": [
                "i2p_enabled", "i2p_address", "i2p_port", "i2p_mixed_mode", "i2p_inbound_quantity", "i2p_outbound_quantity", "i2p_inbound_length", "i2p_outbound_length"
            ],
            "Proxy": [
                "proxy_type", "proxy_ip", "proxy_port", "proxy_auth_enabled", "proxy_username", "proxy_password", "proxy_hostname_lookup", "proxy_bittorrent", "proxy_peer_connections", "proxy_rss", "proxy_misc"
            ],
            "IP Filtering": [
                "ip_filter_enabled", "ip_filter_path", "ip_filter_trackers", "banned_IPs"
            ],
            "Speed": [
                "dl_limit", "up_limit", "alt_dl_limit", "alt_up_limit", "bittorrent_protocol", "limit_utp_rate", "limit_tcp_overhead", "limit_lan_peers", "scheduler_enabled", "schedule_from_hour", "schedule_from_min", "schedule_to_hour", "schedule_to_min", "scheduler_days"
            ],
            "BitTorrent": [
                "dht", "pex", "lsd", "encryption", "anonymous_mode", "max_active_checking_torrents", "queueing_enabled", "max_active_downloads", "max_active_torrents", "max_active_uploads", "dont_count_slow_torrents", "slow_torrent_dl_rate_threshold", "slow_torrent_ul_rate_threshold", "slow_torrent_inactive_timer", "max_ratio_enabled", "max_ratio", "max_seeding_time_enabled", "max_seeding_time", "max_inactive_seeding_time_enabled", "max_inactive_seeding_time", "max_ratio_act", "add_trackers_enabled", "add_trackers", "add_trackers_from_url_enabled", "add_trackers_url", "add_trackers_url_list"
            ],
            "WebUI": [
                "web_ui_domain_list", "web_ui_address", "web_ui_port", "web_ui_upnp", "use_https", "web_ui_https_cert_path", "web_ui_https_key_path", "web_ui_username", "bypass_local_auth", "bypass_auth_subnet_whitelist_enabled", "bypass_auth_subnet_whitelist", "web_ui_max_auth_fail_count", "web_ui_ban_duration", "web_ui_session_timeout", "web_ui_api_key", "alternative_webui_enabled", "alternative_webui_path", "web_ui_clickjacking_protection_enabled", "web_ui_csrf_protection_enabled", "web_ui_secure_cookie_enabled", "web_ui_host_header_validation_enabled", "web_ui_use_custom_http_headers_enabled", "web_ui_custom_http_headers", "web_ui_reverse_proxy_enabled", "web_ui_reverse_proxies_list"
            ],
            "Dynamic DNS": [
                "dyndns_enabled", "dyndns_service", "dyndns_username", "dyndns_password", "dyndns_domain"
            ],
            "RSS": [
                "rss_refresh_interval", "rss_fetch_delay", "rss_max_articles_per_feed", "rss_processing_enabled", "rss_auto_downloading_enabled", "rss_download_repack_proper_episodes", "rss_smart_episode_filters"
            ],
            "Advanced": [
                "resume_data_storage_type", "torrent_content_remove_option", "memory_working_set_limit", "current_network_interface", "current_interface_name", "current_interface_address", "save_resume_data_interval", "save_statistics_interval", "torrent_file_size_limit", "confirm_torrent_recheck", "recheck_completed_torrents", "app_instance_name", "refresh_interval", "resolve_peer_countries", "reannounce_when_address_changed", "enable_embedded_tracker", "embedded_tracker_port", "embedded_tracker_port_forwarding", "mark_of_the_web", "ignore_ssl_errors", "python_executable_path"
            ],
            "libtorrent": [
                "bdecode_depth_limit", "bdecode_token_limit", "async_io_threads", "hashing_threads", "file_pool_size", "checking_memory_use", "disk_cache", "disk_cache_ttl", "disk_queue_size", "disk_io_type", "disk_io_read_mode", "disk_io_write_mode", "enable_coalesce_read_write", "enable_piece_extent_affinity", "enable_upload_suggestions", "send_buffer_watermark", "send_buffer_low_watermark", "send_buffer_watermark_factor", "connection_speed", "socket_send_buffer_size", "socket_receive_buffer_size", "socket_backlog_size", "outgoing_ports_min", "outgoing_ports_max", "upnp_lease_duration", "peer_tos", "utp_tcp_mixed_mode", "hostname_cache_ttl", "idn_support_enabled", "enable_multi_connections_from_same_ip", "validate_https_tracker_certificate", "ssrf_mitigation", "block_peers_on_privileged_ports", "upload_slots_behavior", "upload_choking_algorithm", "announce_to_all_trackers", "announce_to_all_tiers", "announce_ip", "announce_port", "max_concurrent_http_announces", "stop_tracker_timeout", "peer_turnover", "peer_turnover_cutoff", "peer_turnover_interval", "request_queue_size", "dht_bootstrap_nodes"
            ]
        }
        if not args.settings:
            print("Usage: --settings list [category] OR --settings set <key> <value> OR --settings categories")
            sys.exit(1)
        action = args.settings[0]
        if action == "categories":
            print("Available categories:")
            for cat in categories:
                print(f"- {cat}")
        elif action == "list":
            resp = session.get(f"{host}/api/v2/app/preferences")
            if resp.status_code != 200:
                print("Failed to fetch settings.", file=sys.stderr)
                sys.exit(1)
            prefs = resp.json()
            if len(args.settings) > 1:
                cat = args.settings[1]
                if cat not in categories:
                    print(f"Unknown category: {cat}")
                    print("Use --settings categories to see all categories.")
                    sys.exit(1)
                print(f"Settings in category '{cat}':")
                for k in categories[cat]:
                    v = prefs.get(k, "<not set>")
                    print(f"  {k}: {v}")
            else:
                for cat, keys in categories.items():
                    print(f"\n[{cat}]")
                    for k in keys:
                        v = prefs.get(k, "<not set>")
                        print(f"  {k}: {v}")
        elif action == "set":
            if len(args.settings) < 3:
                print("Usage: --settings set <key> <value>")
                sys.exit(1)
            key, value = args.settings[1], args.settings[2]
            
            v_lower = value.lower()
            if v_lower == "true":
                value = True
            elif v_lower == "false":
                value = False
            elif v_lower == "null":
                value = None
            else:
                
                try:
                    if "." in value:
                        value = float(value)
                    else:
                        value = int(value)
                except ValueError:
                    pass
            resp = session.post(f"{host}/api/v2/app/setPreferences", data={"json": json.dumps({key: value})})
            if resp.status_code != 200:
                print("Failed to set setting.", file=sys.stderr)
                sys.exit(1)
            print(f"Set {key} to {value}")
        else:
            print("Unknown settings action. Use 'list', 'set', or 'categories'.")
            sys.exit(1)
        sys.exit(0)

    
    elif args.magnet:
        add_magnet_cli(session, args.host, args.magnet, args.path)
    elif args.torrent:
        add_torrent_cli(session, args.host, args.torrent, args.path)
    elif args.magnet_file:
        add_magnet_file_cli(session, args.host, args.magnet_file, args.path)
    elif args.status:
        print_status(session, args.host)
    elif args.move:
        move_torrents_cli(session, args.host, args.move[0], args.path, args.category)
    elif args.details:
        show_details_cli(session, args.host, args.details)
    elif args.export:
        export_torrents_cli(session, args.host, args.export, args.category, args.tag, args.state)
    elif args.import_dir:
        import_torrents_cli(session, args.host, args.import_dir, args.path)
    elif args.compare:
        compare_torrents_cli(session, args.host, args.user, args.password, args.compare[0], args.compare[1], args.compare[2])
    elif args.list_torrents is not None:
        from src.torrent import torrent_list
        filter_mode = args.list_torrents if args.list_torrents else "All"
        torrents = torrent_list(session, args.host, filter_mode)
        print_torrent_table(torrents, filter_mode)
    elif args.manage_categories is not None:
        if not args.manage_categories:
            print("Usage: --manage-categories list | add <name> [save-path] | delete <name> | edit <name> <save-path>")
            sys.exit(1)
        action = args.manage_categories[0]
        if action == "list":
            manage_categories_cli(session, args.host, "list")
        elif action == "add":
            if len(args.manage_categories) < 2:
                print("Category name is required for add")
                sys.exit(1)
            name = args.manage_categories[1]
            save_path = args.manage_categories[2] if len(args.manage_categories) > 2 else None
            manage_categories_cli(session, args.host, "add", name, save_path)
        elif action == "delete":
            if len(args.manage_categories) < 2:
                print("Category name is required for delete")
                sys.exit(1)
            name = args.manage_categories[1]
            manage_categories_cli(session, args.host, "delete", name)
        elif action == "edit":
            if len(args.manage_categories) < 3:
                print("Category name and save path are required for edit")
                sys.exit(1)
            name = args.manage_categories[1]
            save_path = args.manage_categories[2]
            manage_categories_cli(session, args.host, "edit", name, save_path)
        else:
            print("Invalid action. Use: list, add, delete, or edit")
            sys.exit(1)
    elif args.manage_tags is not None:
        if not args.manage_tags:
            print("Usage: --manage-tags list | add <tag> <hashes> | remove <tag> <hashes> | delete <tag>")
            sys.exit(1)
        action = args.manage_tags[0]
        if action == "list":
            manage_tags_cli(session, args.host, "list")
        elif action == "add":
            if len(args.manage_tags) < 3:
                print("Tag name and torrent hashes are required for add")
                sys.exit(1)
            tag_name = args.manage_tags[1]
            hashes = args.manage_tags[2]
            manage_tags_cli(session, args.host, "add", tag_name, hashes)
        elif action == "remove":
            if len(args.manage_tags) < 3:
                print("Tag name and torrent hashes are required for remove")
                sys.exit(1)
            tag_name = args.manage_tags[1]
            hashes = args.manage_tags[2]
            manage_tags_cli(session, args.host, "remove", tag_name, hashes)
        elif action == "delete":
            if len(args.manage_tags) < 2:
                print("Tag name is required for delete")
                sys.exit(1)
            tag_name = args.manage_tags[1]
            manage_tags_cli(session, args.host, "delete", tag_name)
        else:
            print("Invalid action. Use: list, add, remove, or delete")
            sys.exit(1)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
