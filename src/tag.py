def tag_cli(subparsers):
    tag_parser = subparsers.add_parser("tag", help="Tag management")
    tag_sub = tag_parser.add_subparsers(dest="tag_cmd", required=True)
    add_parser = tag_sub.add_parser("add", help="Add tag")
    add_parser.add_argument('tag', help='Tag name')
    add_parser.set_defaults(func=tag_add)

    delete_parser = tag_sub.add_parser("delete", help="Delete tag")
    delete_parser.add_argument('tag', help='Tag name')
    delete_parser.set_defaults(func=tag_delete)

    list_parser = tag_sub.add_parser("list", help="List tags")
    list_parser.set_defaults(func=tag_list)

def tag_add(args, session):
    resp = session.post(f"{args.host}/api/v2/torrents/addTags", data={'tags': args.tag, 'hashes': ''})
    if resp.status_code == 200:
        print(f"Tag '{args.tag}' added.")
    else:
        print("Failed to add tag:", resp.text)

def tag_delete(args, session):
    resp = session.post(f"{args.host}/api/v2/torrents/removeTags", data={'tags': args.tag, 'hashes': ''})
    if resp.status_code == 200:
        print(f"Tag '{args.tag}' deleted.")
    else:
        print("Failed to delete tag:", resp.text)

def tag_list(args, session):
    resp = session.get(f"{args.host}/api/v2/torrents/tags")
    if resp.status_code == 200:
        tags = resp.json()
        for tag in tags:
            print(tag)
    else:
        print("Failed to list tags:", resp.text)
