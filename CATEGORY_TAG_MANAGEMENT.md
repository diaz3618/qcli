
# qBittorrent CLI (qcli) - Category and Tag Management

## Features Overview

### Category Management (`--manage-categories`)

Organize torrents into categories for easier management and automation.

#### Commands:

**List all categories:**
```bash
qcli.py --manage-categories list
```

**Add a new category:**
```bash
# Without save path
qcli.py --manage-categories add "CategoryName"

# With save path
qcli.py --manage-categories add "CategoryName" "/path/to/save"
```

**Edit category save path:**
```bash
qcli.py --manage-categories edit "CategoryName" "/new/save/path"
```

**Delete a category:**
```bash
qcli.py --manage-categories delete "CategoryName"
```

#### Example Output:
```
$ qcli.py --manage-categories list
Categories:
Name                 Save Path                                         
------------------------------------------------------------------------
CategoryName         /path/to/save                                     
OtherCategory        /other/path                                       
Unsorted                                                                
```

### Tag Management (`--manage-tags`)

Label and filter torrents using tags for flexible organization.

#### Commands:

**List all tags:**
```bash
qcli.py --manage-tags list
```

**Add tag to specific torrents:**
```bash
# Single torrent
qcli.py --manage-tags add "TagName" <torrent_hash>

# Multiple torrents (comma-separated)
qcli.py --manage-tags add "TagName" <hash1>,<hash2>,<hash3>

# Add to ALL torrents
qcli.py --manage-tags add "TagName" all
```

**Remove tag from torrents:**
```bash
# Remove from specific torrents
qcli.py --manage-tags remove "TagName" <torrent_hash>

# Remove from all torrents
qcli.py --manage-tags remove "TagName" all
```

**Delete tag completely:**
```bash
# Removes tag from all torrents and deletes it
qcli.py --manage-tags delete "TagName"
```

#### Example Output:
```
$ qcli.py --manage-tags list
Available tags:
  - TagName
  - AnotherTag
  - Downloaded
  - Archived
```

### Integration with Other Features

Category and tag management work with existing commands:

**Export with filters:**
```bash
# Export by category
qcli.py --export /backup --category "CategoryName"

# Export by tag
qcli.py --export /backup --tag "TagName"
```

**Move torrents to category:**
```bash
qcli.py --move <torrent_hash> --category "CategoryName"
```

### Error Handling

All commands include robust error handling:
- Input validation for required parameters
- Clear error messages for invalid operations
- Proper HTTP status code checking
- Graceful handling of missing categories/tags

### API Compatibility

Uses official qBittorrent WebUI API endpoints:
- Categories: `/api/v2/torrents/categories`, `/api/v2/torrents/createCategory`, `/api/v2/torrents/removeCategories`, `/api/v2/torrents/editCategory`
- Tags: `/api/v2/torrents/tags`, `/api/v2/torrents/addTags`, `/api/v2/torrents/removeTags`