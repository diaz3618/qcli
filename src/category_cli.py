def manage_categories_cli(session, host, action, name=None, save_path=None):
    """
    Manage qBittorrent categories
    """
    if action == "list":
        try:
            resp = session.get(f"{host}/api/v2/torrents/categories")
            resp.raise_for_status()
            categories = resp.json()
            
            if not categories:
                print("No categories found.")
                return
                
            print("Categories:")
            print(f"{'Name':<20} {'Save Path':<50}")
            print("-" * 72)
            
            for cat_name, info in categories.items():
                save_path_str = info.get('savePath', '')
                print(f"{cat_name:<20} {save_path_str:<50}")
                
        except Exception as e:
            print(f"Error fetching categories: {e}")
            exit(1)
            
    elif action == "add":
        if not name:
            print("Category name is required for add operation")
            exit(1)
            
        try:
            data = {'category': name}
            if save_path:
                data['savePath'] = save_path
                
            resp = session.post(f"{host}/api/v2/torrents/createCategory", data=data)
            resp.raise_for_status()
            
            if resp.status_code == 200:
                print(f"Category '{name}' added successfully.")
                if save_path:
                    print(f"  Save path: {save_path}")
            else:
                print(f"Failed to add category: {resp.text}")
                exit(1)
                
        except Exception as e:
            print(f"Error adding category: {e}")
            exit(1)
            
    elif action == "delete":
        if not name:
            print("Category name is required for delete operation")
            exit(1)
            
        try:
            resp = session.post(f"{host}/api/v2/torrents/removeCategories", 
                              data={'categories': name})
            resp.raise_for_status()
            
            if resp.status_code == 200:
                print(f"Category '{name}' deleted successfully.")
            else:
                print(f"Failed to delete category: {resp.text}")
                exit(1)
                
        except Exception as e:
            print(f"Error deleting category: {e}")
            exit(1)
            
    elif action == "edit":
        if not name:
            print("Category name is required for edit operation")
            exit(1)
        if not save_path:
            print("Save path is required for edit operation")
            exit(1)
            
        try:
            data = {'category': name, 'savePath': save_path}
            resp = session.post(f"{host}/api/v2/torrents/editCategory", data=data)
            resp.raise_for_status()
            
            if resp.status_code == 200:
                print(f"Category '{name}' updated successfully.")
                print(f"  New save path: {save_path}")
            else:
                print(f"Failed to edit category: {resp.text}")
                exit(1)
                
        except Exception as e:
            print(f"Error editing category: {e}")
            exit(1)
            
    else:
        print("Invalid action. Use: list, add, delete, or edit")
        exit(1)