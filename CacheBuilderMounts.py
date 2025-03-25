import requests
import re
import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__)) # Setup paths
ID_LIST_FILE = os.path.join(script_dir, "missingMounts.json") #File that will be read from (SimpleArmory script pastes here)
CACHE_FILE = os.path.join(script_dir, "Structured_Cache.json") #File where the script will insert all the mounts in a structured manner

headers = {"User-Agent": "Mozilla/5.0"}

def extract_icon_from_item_html(html):
    match = re.search(r'https://wow\.zamimg\.com/images/wow/icons/large/[^"]+\.jpg', html)     #The images on wowhead have different size variants. This gathers the large variant.
    if match:
        return match.group(0) #Returns the image
    return None #Error handling

def get_item_data(item_id):
    url = f"https://www.wowhead.com/item={item_id}" #The Wowhead link
    response = requests.get(url, headers=headers)
    if response.status_code != 200: #Code 200 (requests library) means the fetch was successful
        return { #Error handling
            "id": item_id,
            "name": "[Unknown Item]",
            "icon": None,
            "link": url
        }

    html = response.text #Runs if requests code is 200


    name_match = re.search(r'"name":"(.*?)"', html) #Fetches the name of the item
    name = name_match.group(1) if name_match else "[Unknown Item]" #Error handling

    icon_url = extract_icon_from_item_html(html) #Gathers the image

    return { #Returns pastes relevant data
        "id": item_id,
        "name": name,
        "icon": icon_url,
        "link": url
    }

try:
    with open(ID_LIST_FILE, "r") as f: #Refers to the JSON file defined at the top of the script
        id_list = json.load(f) #Turns it into a list
        id_list = [int(x) for x in id_list if isinstance(x, int) or (isinstance(x, str) and str(x).isdigit())] #Cleans up mixed types in the list
except Exception as e: #Error handling
    print(f"Failed to load ID list: {e}")
    id_list = []

if os.path.exists(CACHE_FILE): #Load existing cache if available
    try:
        with open(CACHE_FILE, "r") as f:
            ALL_Mounts_Structured_Cache = json.load(f)
    except Exception as e:
        print(f"Failed to load existing cache: {e}")
        ALL_Mounts_Structured_Cache = {}
else:
    ALL_Mounts_Structured_Cache = {}

for item_id in id_list: #Skips items that are already cached so you don't have to waste resources
    item_id_str = str(item_id)
    if item_id_str in ALL_Mounts_Structured_Cache:
        print(f"Skipping item {item_id} (already cached).")
        continue

    print(f"Fetching item {item_id}...")
    item_data = get_item_data(item_id)
    ALL_Mounts_Structured_Cache[item_id_str] = item_data

    with open(CACHE_FILE, "w") as f: #Save to file after each item
        json.dump(ALL_Mounts_Structured_Cache, f, indent=2)

print(f"\nDone. Saved {len(ALL_Mounts_Structured_Cache)} items to {CACHE_FILE}")
