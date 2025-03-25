from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
import re
import time
import json

# Character info (This is the only place you'll have to insert your info)
Region = "eu" #Can be "eu" or "us" 
Realm = "dragonblight" #Replace "dragonblight" with your realm
Name = "azur" #Replace "azur" with your name

# Configure Edge options
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1280,800")
driver = None

#Use webdriver-manager to auto-download EdgeDriver
try: #Installation to use selenium
    driver = webdriver.Edge(
        service=EdgeService(EdgeChromiumDriverManager().install()),
        options=options
    )
except: #In case it's already installed
    driver = webdriver.Edge(options=options)

url = f"https://simplearmory.com/#/{Region}/{Realm}/{Name}/collectable/mounts" #Armory page
driver.get(url) #Fetches the page

print("Waiting for mount data to load...")
time.sleep(10) #Give a few seconds for the script to catch up

elements = driver.find_elements(By.CSS_SELECTOR, "a.thumbnail.notCollected") #a.thumbnail.notCollected in the websites HTML means you don't have the mount

missing_mounts = []
for el in elements: #Runs for missing mount
    href = el.get_attribute("href")
    match = re.search(r'item=(\d+)', href)
    item_id = match.group(1) if match else None
    img = el.find_element(By.TAG_NAME, "img")
    icon = img.get_attribute("src")
    alt = img.get_attribute("alt")
    if item_id:
        missing_mounts.append({
            "item_id": item_id, #Mount ID
            "icon_alt": alt, #Mount name
            "icon_url": icon, #Mount icon
            "wowhead_url": "https:" + href #Wowhead link
        })

driver.quit()

print(f"\n Found {len(missing_mounts)} uncollected mounts:\n") #Debugging
for mount in missing_mounts:
    print(f"ID {mount['item_id']}: {mount['icon_alt']} → {mount['wowhead_url']}") #Debugging

item_ids = [int(m['item_id']) for m in missing_mounts]
with open("missingMounts.json", "w") as f: #Pastes a list of IDs into "missingMounts.json"
    json.dump(item_ids, f, indent=4)
print("\n Saved IDs in missingMounts.json")
