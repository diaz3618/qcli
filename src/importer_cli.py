import os

def import_torrents_cli(session, host, source_dir):
    if not source_dir or not os.path.isdir(source_dir):
        print("Error: --import-dir must be a valid directory containing .torrent files.")
        exit(2)
    log_path = os.path.join(source_dir, "import_errors.log")
    def log_error(msg):
        with open(log_path, "a") as logf:
            logf.write(msg + "\n")
    for fname in os.listdir(source_dir):
        if fname.endswith('.torrent'):
            fpath = os.path.join(source_dir, fname)
            try:
                with open(fpath, 'rb') as f:
                    files = {'torrents': f}
                    resp = session.post(f"{host}/api/v2/torrents/add", files=files)
                if resp.status_code == 200:
                    print(f"Imported: {fname}")
                else:
                    err_msg = f"Failed to import {fname}: {resp.text}"
                    print(err_msg)
                    log_error(err_msg)
            except Exception as e:
                err_msg = f"Error importing {fname}: {e}"
                print(err_msg)
                log_error(err_msg)
