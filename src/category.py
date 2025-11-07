def category_cli(subparsers):
    cat_parser = subparsers.add_parser("category", help="Category management")
    cat_sub = cat_parser.add_subparsers(dest="cat_cmd", required=True)
    add_parser = cat_sub.add_parser("add", help="Add category")
    add_parser.add_argument('name', help='Category name')
    add_parser.add_argument('--save-path', help='Category default save path')
    add_parser.set_defaults(func=category_add)

    delete_parser = cat_sub.add_parser("delete", help="Delete category")
    delete_parser.add_argument('name', help='Category name')
    delete_parser.set_defaults(func=category_delete)

    edit_parser = cat_sub.add_parser("edit", help="Edit category")
    edit_parser.add_argument('name', help='Category name')
    edit_parser.add_argument('--save-path', help='New save path')
    edit_parser.set_defaults(func=category_edit)

    list_parser = cat_sub.add_parser("list", help="List categories")
    list_parser.set_defaults(func=category_list)

def category_add(args, session):
    data = {'category': args.name}
    if args.save_path:
        data['savePath'] = args.save_path
    resp = session.post(f"{args.host}/api/v2/categories/create", data=data)
    if resp.status_code == 200:
        print(f"Category '{args.name}' added.")
    else:
        print("Failed to add category:", resp.text)

def category_delete(args, session):
    resp = session.post(f"{args.host}/api/v2/categories/remove", data={'category': args.name})
    if resp.status_code == 200:
        print(f"Category '{args.name}' deleted.")
    else:
        print("Failed to delete category:", resp.text)

def category_edit(args, session):
    data = {'category': args.name}
    if args.save_path:
        data['savePath'] = args.save_path
    resp = session.post(f"{args.host}/api/v2/categories/edit", data=data)
    if resp.status_code == 200:
        print(f"Category '{args.name}' edited.")
    else:
        print("Failed to edit category:", resp.text)

def category_list(args, session):
    resp = session.get(f"{args.host}/api/v2/categories/list")
    if resp.status_code == 200:
        categories = resp.json()
        for name, info in categories.items():
            print(f"{name}: {info.get('savePath', '')}")
    else:
        print("Failed to list categories:", resp.text)
