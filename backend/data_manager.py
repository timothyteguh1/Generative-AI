import json
import time
import os
from datetime import datetime

def save_recipe(recipe_data):
    """Simpan resep jadi JSON (Dataset Resep)"""
    if not recipe_data: return
    
    filename = f"data/recipes/resep_{int(time.time())}.json"
    with open(filename, 'w') as f:
        json.dump(recipe_data, f, indent=4)
    return filename

def log_user_prompt(user_input, action_type):
    """Simpan history chat user (Dataset Prompt)"""
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": action_type,
        "prompt": user_input
    }
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"data/logs/log_{date_str}.json"
    
    existing_data = []
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                existing_data = json.load(f)
        except: pass
    
    existing_data.append(log_entry)
    
    with open(filename, 'w') as f:
        json.dump(existing_data, f, indent=4)