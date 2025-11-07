from src.color import color_state

def print_torrent_table(torrents, filter_mode):
    print(f"Listing {len(torrents)} torrents (filter: {filter_mode})\n")
    print(f"{'Hash':<40}  {'Name':<30}  {'State':<16}")
    print("-"*89)
    for t in torrents:
        name = t['name']
        if len(name) > 27:
            name = name[:27] + '...'
        state = t['state']
        state_str = color_state(state)
        print(f"{t['hash']:<40}  {name:<30}  {state_str}")
