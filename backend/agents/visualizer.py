import ollama
import json
import urllib.parse
import random

# Gunakan model yang Anda punya
MODEL_NAME = "llama3"

def generate_and_save_images(dish_name, steps):
    print(f"\n[VISUALIZER] 🔗 Menganalisis Konteks Visual per Langkah...")
    
    steps_text = [s['instruction'] for s in steps]
    
    # --- 1. PROMPT ENGINEERING YANG LEBIH CERDAS ---
    # Kita minta AI menentukan:
    # - action: Apa yang dilakukan (misal: chopping, boiling)
    # - object: Bahan apa yang TERLIHAT SAAT ITU (misal: raw onions, boiling water)
    # - phase: Apakah ini PREP (persiapan), COOK (masak di kompor/oven), atau SERVE (penyajian)
    
    prompt_gen = f"""
    You are a visual director. For the recipe "{dish_name}", analyze these steps visually.
    
    Steps: {steps_text}
    
    For each step, output a JSON object with:
    1. "short_action": max 3 words (e.g., "Slicing onions", "Stirring sauce").
    2. "visual_focus": specific ingredients visible NOW (e.g., "raw beef chunks, knife", "bubbling soup").
    3. "phase": choose strictly one of ["PREP", "COOK", "SERVE"].
       - PREP: cutting, washing, mixing raw ingredients.
       - COOK: heating, frying, baking, boiling.
       - SERVE: plating, garnishing, eating.
    
    Output STRICT JSON format: {{ "scenes": [ {{...}}, {{...}} ] }}
    """
    
    try:
        response = ollama.chat(
            model=MODEL_NAME,
            format='json',
            messages=[{'role': 'user', 'content': prompt_gen}]
        )
        scenes = json.loads(response['message']['content']).get('scenes', [])
    except Exception as e:
        print(f"Error parsing AI response: {e}")
        # Fallback manual jika AI gagal
        scenes = [{"short_action": f"Step {i+1}", "visual_focus": "ingredients", "phase": "COOK"} for i in range(len(steps))]

    # Pastikan jumlah scene sama dengan steps
    if len(scenes) < len(steps):
        diff = len(steps) - len(scenes)
        scenes.extend([{"short_action": "Cooking", "visual_focus": "food", "phase": "COOK"}] * diff)

    image_urls = []
    
    # --- 2. KONSTRUKSI PROMPT GAMBAR (DYNAMIC CONTEXT) ---
    for i, scene in enumerate(scenes):
        step_num = i + 1
        
        action = scene.get('short_action', 'Cooking')
        objects = scene.get('visual_focus', 'food')
        phase = scene.get('phase', 'COOK')
        
        # Base Style (Konsisten)
        style = "hyper-realistic, 8k, cinematic lighting, food photography, sharp focus, f/1.8 aperture"
        
        # Logika Prompt Berdasarkan Phase dari AI
        if phase == "PREP":
            # Fokus: Meja dapur, talenan, bahan mentah. JANGAN tampilkan masakan jadi.
            environment = "on wooden cutting board, kitchen counter context, raw ingredients, bright natural light"
            full_prompt = f"Close up shot of {action}, featuring {objects}, {environment}, {style}"
            
        elif phase == "COOK":
            # Fokus: Kompor, uap, panci, transformasi.
            environment = "inside cookware, steam rising, stove fire background, cooking process, sizzling texture"
            full_prompt = f"Action shot of {action}, {objects}, {environment}, {style}"
            
        elif phase == "SERVE":
            # Fokus: Hasil akhir cantik.
            environment = f"final dish {dish_name}, restaurant plating, bokeh background, garnished perfectly"
            full_prompt = f"Professional food photo of {dish_name}, {environment}, {style}"
        
        else:
            # Fallback
            full_prompt = f"{action} {objects}, cooking {dish_name}, {style}"

        # --- 3. Generate URL ---
        print(f"✅ Step {step_num} [{phase}]: {full_prompt[:60]}...") # Debugging log
        
        safe_prompt = urllib.parse.quote(full_prompt)
        # Gunakan seed acak agar variasi, tapi bisa diset fix jika ingin konsistensi gaya
        seed = random.randint(100, 99999) 
        
        # Tambahkan 'nologo=true' dan model 'flux' (bagus untuk prompt kompleks)
        url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1024&height=768&model=flux&nologo=true&seed={seed}"
        
        image_urls.append(url)

    return image_urls