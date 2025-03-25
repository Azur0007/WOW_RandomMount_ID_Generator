import tkinter as tk
import random
import json
import os
import webbrowser
from PIL import Image, ImageTk
from io import BytesIO
import requests

BG = "#1e1e1e"
FG = "#ffffff"
BOX = "#2b2b2b"

script_dir = os.path.dirname(os.path.abspath(__file__)) #Path to script folder
CACHE_FILE = os.path.join(script_dir, "Structured_Cache.json") #Reads from Structured_Cache.json

try: # Load cache from file
    with open(CACHE_FILE, "r") as f:
        structured_cache = json.load(f)
except (FileNotFoundError, json.JSONDecodeError): #Error handling
    structured_cache = {}

valid_ids = list(structured_cache.keys()) #Index
valid_ids = [int(i) for i in valid_ids] #Figures out how many IDs there are in Structured_cache

def load_icon_from_url(url): #Gets the image for the tkinter window
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content)).resize((24, 24))
        return ImageTk.PhotoImage(img)
    except: #Error handling
        return None

def open_wowhead(url): #If the name is clicked, this opens a link to wowhead
    webbrowser.open_new_tab(url)

def remove_item(item_id, frame): #If the remove button is pressed, this deletes the entry from structured_cache
    if str(item_id) in structured_cache:
        structured_cache.pop(str(item_id))
        with open(CACHE_FILE, "w") as f:
            json.dump(structured_cache, f, indent=2)
        frame.destroy()

def generate_items(): #This clears the list when you click generate continuously
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    try:
        count = int(entry.get())
    except ValueError: #Error handling
        tk.Label(scrollable_frame, text="Enter a valid number.", font=("Segoe UI", 10), bg=BG, fg=FG).pack()
        scroll_canvas.yview_moveto(0)
        return

    if count <= 0: #Error handling
        tk.Label(scrollable_frame, text="Number must be > 0.", font=("Segoe UI", 10), bg=BG, fg=FG).pack()
        scroll_canvas.yview_moveto(0)
        return

    available = list(structured_cache.items())
    random.shuffle(available)
    selected = available[:count]

    for item_id, info in selected: #Gets the info of each mount
        name = info.get("name", "[Unknown Item]")
        icon_url = info.get("icon", "")
        wowhead_link = info.get("wowhead_link", f"https://www.wowhead.com/item={item_id}")

        frame = tk.Frame(scrollable_frame, bg=BOX, bd=1, relief="solid")
        frame.pack(fill="x", padx=12, pady=6, ipady=4)

        icon_img = load_icon_from_url(icon_url) if icon_url else None
        if icon_img:
            icon_label = tk.Label(frame, image=icon_img, bg=BOX)
            icon_label.image = icon_img
            icon_label.pack(side="left", padx=(8, 6), pady=5)

        label = tk.Label(
            frame,
            text=f"ID {item_id}: {name}",
            font=("Segoe UI", 11, "underline"),
            anchor="w",
            bg=BOX,
            fg="#ffaa55" if name.startswith("[Unknown") else "#4da6ff",
            cursor="hand2"
        )
        label.pack(side="left", padx=4, pady=5)
        label.bind("<Button-1>", lambda e, link=wowhead_link: open_wowhead(link))

        btn = tk.Button(
            frame,
            text="Remove",
            font=("Segoe UI", 10),
            bg="#cc3333",
            fg="white",
            relief="flat",
            activebackground="#dd5555",
            command=lambda iid=item_id, f=frame: remove_item(iid, f)
        )
        btn.pack(side="right", padx=10)

    scroll_canvas.yview_moveto(0)
    
root = tk.Tk()
root.title("Mount viewer")
root.geometry("700x600")
root.configure(bg=BG)

tk.Label(root, text="Mount ID Generator", font=("Segoe UI", 18, "bold"), bg=BG, fg=FG).pack(pady=(20, 10))
tk.Label(root, text="How many Mount IDs to generate?", font=("Segoe UI", 12), bg=BG, fg=FG).pack()

entry_frame = tk.Frame(root, bg=BG)
entry_frame.pack(pady=5)

entry = tk.Entry(entry_frame, font=("Segoe UI", 11), width=10, bg="#333333", fg=FG, insertbackground=FG)
entry.pack(side="left", padx=(0, 10))
entry.insert(0, "5")

tk.Button(
    entry_frame,
    text="Generate",
    font=("Segoe UI", 11),
    bg="#289de3",
    fg="white",
    activebackground="#1c7dc2",
    activeforeground="white",
    highlightthickness=0,
    borderwidth=0,
    relief="flat",
    command=generate_items
).pack(side="left")

scroll_frame = tk.Frame(root, bg=BG)
scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

scroll_canvas = tk.Canvas(scroll_frame, bg=BG, highlightthickness=0)
scroll_canvas.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(scroll_frame, orient="vertical", command=scroll_canvas.yview)
scrollbar.pack(side="right", fill="y")

scrollable_frame = tk.Frame(scroll_canvas, bg=BG)
window_id = scroll_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

def resize_scrollable_frame(event):
    canvas_width = event.width
    scroll_canvas.itemconfig(window_id, width=canvas_width)

scroll_canvas.bind("<Configure>", resize_scrollable_frame)

def update_scroll_region(event):
    scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))

scrollable_frame.bind("<Configure>", update_scroll_region)

scroll_canvas.configure(yscrollcommand=scrollbar.set)

root.mainloop()
