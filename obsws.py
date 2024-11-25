import obsws_python as obs
import requests
import time

# pass conn info if not in config.toml
cl = obs.ReqClient(host='localhost', port=4455, password='password', timeout=3)

# Toggle the mute state of your Mic input
cl.toggle_input_mute('Mic/Aux')

scene_items = cl.get_scene_item_list('In-Game Layout - Horizontal')
with open('scene_items.json', 'w') as f:
    f.write(str(scene_items.scene_items))

# Now access the 'scene_items' attribute directly (not 'items')
for item in scene_items.scene_items:  # Access the scene_items attribute
    print(f"Source Name: {item['sourceName']}")
    print(f"Scene Item ID: {item['sceneItemId']}")
    print(f"Item Enabled: {item['sceneItemEnabled']}")
    print("------")

# Function to handle follow events and play animation
def alert(sceneTextItemId, sceneImageItemId, username, type):
    # Show the source (e.g., FollowAnimation in OBS)
    cl.set_input_settings(name="FollowerText", settings={"text": f"New {type}: {username}"}, overlay=True)
    cl.set_scene_item_enabled(scene_name="In-Game Layout - Horizontal", item_id=sceneTextItemId, enabled=True)
    cl.set_scene_item_enabled(scene_name="In-Game Layout - Horizontal", item_id=sceneImageItemId, enabled=True)
    # Hide it after 5 seconds (or the length of your animation)
    time.sleep(5)
    cl.set_scene_item_enabled(scene_name="In-Game Layout - Horizontal", item_id=sceneTextItemId, enabled=False)
    cl.set_scene_item_enabled(scene_name="In-Game Layout - Horizontal", item_id=sceneImageItemId, enabled=False)
