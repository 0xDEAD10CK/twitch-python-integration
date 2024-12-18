import obsws_python as obs
from dataclasses import asdict
import requests
import time
from dotenv import load_dotenv
import os

load_dotenv()

OBS_PASSWORD = os.getenv('OBS_PASSWORD')
LIST_SCENES = ["In-Game Layout - Horizontal"] 

# pass conn info if not in config.toml
cl = obs.ReqClient(host='localhost', port=4455, password=OBS_PASSWORD, timeout=3)

scene_items = cl.get_scene_item_list('In-Game Layout - Horizontal')
with open('scene_items.json', 'w') as f:
    f.write(str(scene_items.scene_items))

# Now access the 'scene_items' attribute directly (not 'items')
for item in scene_items.scene_items:  # Access the scene_items attribute
    print(f"Source Name: {item['sourceName']}")
    print(f"Scene Item ID: {item['sceneItemId']}")
    print(f"Item Enabled: {item['sceneItemEnabled']}")
    print("------")

def spin_chat():
    i = 0
    while True:
        cl.set_input_settings(name="Chat", settings={"gradient_dir": float(i)}, overlay=True)
        time.sleep(0.05)
        i += 1
        if i == 360:
            i = 0


# Function to handle follow events and play animation
def alert(sceneTextItemId, sceneImageItemId, sceneSoundItemId, username, type):
    # Show the source (e.g., FollowAnimation in OBS)
    cl.set_input_settings(name="FollowerText", settings={"text": f"New {type}: {username}"}, overlay=True)
    cl.set_scene_item_enabled(scene_name="In-Game Layout - Horizontal", item_id=sceneTextItemId, enabled=True)
    cl.set_scene_item_enabled(scene_name="In-Game Layout - Horizontal", item_id=sceneImageItemId, enabled=True)
    cl.set_scene_item_enabled(scene_name="In-Game Layout - Horizontal", item_id=sceneSoundItemId, enabled=True)
    # Hide it after 5 seconds (or the length of your animation)
    time.sleep(5)
    cl.set_scene_item_enabled(scene_name="In-Game Layout - Horizontal", item_id=sceneTextItemId, enabled=False)
    cl.set_scene_item_enabled(scene_name="In-Game Layout - Horizontal", item_id=sceneImageItemId, enabled=False)
    cl.set_scene_item_enabled(scene_name="In-Game Layout - Horizontal", item_id=sceneSoundItemId, enabled=False)
