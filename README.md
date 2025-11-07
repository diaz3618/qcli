
# qcli

![Python](https://img.shields.io/badge/python-3.13%2B-blue)

qcli is a useful cli tool for managing torrents on a remote qBittorrent server via its WebUI API. It supports adding magnet links and .torrent files, batch operations, exporting/importing torrents, server status, moving torrents, and more.

## Disclaimer

- There's a few defaults in *qcli.py*, make sure you change those. They're there to make my life easier.
- It's a relatively new project, there might be some errors, I'll work on it with time.

## Features

- Add magnet links or .torrent files to your qBittorrent server
- Batch add magnets from a file
- Export and import magnet links for backup or migration
- Move torrents to new save paths or categories
- View server status (health, free space, active downloads)
- Show detailed info for a specific torrent
- Compare torrents between two servers

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
- `--path` Download save path on server
- `--host` qBittorrent WebUI host URL (default: http://172.16.0.20:8080).
- `--user` qBittorrent WebUI username (default: admin)
- `--pass` qBittorrent WebUI password (default: adminadmin)
- `--status` Show server health, free space, and active downloads
- `--move` Move torrents to new save path or category
- `--details` Show full info for a specific torrent
- `--export` Export all magnet links to a single file named with the current date and time, e.g. `20251104-1304_magnets.txt`, in the specified directory. .torrent export is not supported.
## Exporting magnet links

When using `--export`, qcli will export all magnet links for your torrents to a single file named with the current date and time, e.g. `20251104-1304_magnets.txt`, in the specified directory. Each magnet link will be written on its own line. Exporting `.torrent` files is not supported.

## Logging and Error Handling

qcli uses Python's logging module for all output and error handling. Errors in submodules raise exceptions and are handled in the main CLI. All status, move, and details operations log their output.
- `--import-dir` Import all .torrent files from directory
- `--compare` Compare torrents between two servers

## Example

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

## Contributing

Not much to contribute to, but if you have an idea or find a bug, let me know.

## License

This project is licensed under the MIT License.

*Do whatever you want with it*