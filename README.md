# qcli

![Python](https://img.shields.io/badge/python-3.13%2B-blue)

qcli is a useful cli tool for managing torrents on a remote qBittorrent server via its WebUI API. It supports adding magnet links and .torrent files, batch operations, exporting/importing torrents, server status, moving torrents, and more.

## Disclaimer

- There's a few defaults in *qcli.py*, make sure you change those. They're there to make my life easier.
- It's a relatively new project, there might be some errors, I'll work on it with time.


## Features

- Add magnet links or .torrent files to your qBittorrent server
- Batch add magnets from a file
- List all torrents in a color-coded table, with filtering by state
- Export all magnet links for backup or migration
- Import all .torrent files from a directory
- Move torrents to new save paths or categories
- View server status (health, free space, active downloads)
- Show detailed info for a specific torrent
- Compare torrents between two servers
- Manage qBittorrent WebUI settings, organized by category, with options to list categories, view settings per category, and change any setting from the CLI
- **Organize and label your torrents with categories and tags** (see [CATEGORY_TAG_MANAGEMENT.md](./CATEGORY_TAG_MANAGEMENT.md) for full details)

## Installation

Clone this repository and install dependencies:

```bash
git clone https://github.com/diaz3618/qcli.git
cd qcli
pip install -r requirements.txt
```

## Usage

Run the CLI tool with your desired options:

```bash
./qcli.py --magnet "magnet:?xt=..." --path /downloads
./qcli.py --torrent file.torrent --path /downloads
./qcli.py --magnet-file magnets.txt --path /downloads
./qcli.py --status
./qcli.py --move HASH1,HASH2 --path /newpath
./qcli.py --details HASH
./qcli.py --export /path/to/exported_magnets
./qcli.py --import-dir /path/to/torrents
./qcli.py --compare HOST USER PASS
```


## Options

- `--magnet` Magnet link to add
- `--torrent` Path to .torrent file to add
- `--magnet-file` Path to file with magnet links (one per line)
- `--list-torrents [FILTER]` List torrents, optionally filtered by state: All, Active, Downloading, Seeding, Completed, Stopped, Stalled, Errored
- `--path` Download save path on server
- `--host` qBittorrent WebUI host URL (default: http://localhost:8080)
- `--user` qBittorrent WebUI username (default: admin)
- `--pass` qBittorrent WebUI password (default: adminadmin)
- `--status` Show server health, free space, and active downloads
- `--move` Move torrents to new save path or category
- `--details` Show full info for a specific torrent
- `--export` Export all magnet links to a single file named with the current date and time, in the specified directory
- `--import-dir` Import all .torrent files from directory
- `--compare` Compare torrents between two servers
- `--settings` Manage qBittorrent WebUI settings
- `--manage-categories` Organize torrents into categories (add, edit, delete, list)
- `--manage-tags` Label and filter torrents with tags (add, remove, delete, list)


## Example Usage

Add a magnet link:
```bash
./qcli.py --magnet "magnet:?xt=urn:btih:..." --path /downloads
```

Export all torrents:
```bash
./qcli.py --export /path/to/exported_torrents
```

Show server status:
```bash
./qcli.py --status
```

Organize torrents with categories:
```bash
./qcli.py --manage-categories add "Movies" /downloads/movies
./qcli.py --manage-categories list
```

Label torrents with tags:
```bash
./qcli.py --manage-tags add "favorite" a1b2c3d4e5f6...
./qcli.py --manage-tags list
```

For more advanced category and tag management, see [CATEGORY_TAG_MANAGEMENT.md](./CATEGORY_TAG_MANAGEMENT.md).


## WebUI Settings Management

You can view and change all qBittorrent WebUI settings, organized by category:

- List all categories:
	```bash
	./qcli.py --settings categories
	```
- List all settings in a category:
	```bash
	./qcli.py --settings list <category>
	```
- List all settings, grouped by category:
	```bash
	./qcli.py --settings list
	```
- Change a setting:
	```bash
	./qcli.py --settings set <key> <value>
	```

Values for booleans (`true`/`false`), numbers, and `null` are automatically converted to the correct type. All changes are sent in the correct format for the qBittorrent WebUI API.


## Contributing

This project is always open to ideas, improvements, and bug reports. If you have a suggestion or run into an issue, open an issue or pull request—let's make torrent management better for everyone.


## License

MIT License. Use, modify, share, and enjoy.