import google.generativeai as genai
import json
import os
import requests
import time
import threading
import shutil
import random
from concurrent.futures import ThreadPoolExecutor
from config import configure_ai

configure_ai()
# Gunakan model flash yang cepat untuk visual prompt
try:
    model = genai.GenerativeModel('models/gemini-2.5-flash')
except:
    model = genai.GenerativeModel('models/gemini-1.5-flash')

# Folder simpan gambar
IMAGE_DIR = "saved_images"
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

fast_config = genai.types.GenerationConfig(
    temperature=0.2, response_mime_type="application/json"
)

def _download_single_image(args):
    """
    Download 1 gambar dengan logika Anti-429 (Rate Limit Handling).
    """
    prompt, path, idx = args
    
    # TRICK: Potong prompt jadi maksimal 10 kata agar URL pendek & ringan
    short_prompt = " ".join(prompt.split()[:10]) 
    safe_prompt = short_prompt.replace(" ", "%20")
    
    # Random seed agar gambar variatif
    seed = random.randint(1000, 99999) + idx
    
    # URL Pollinations (Model Turbo)
    url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=512&height=384&model=turbo&nologo=true&seed={seed}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) ChefBot/1.0"
    }

    # --- RETRY LOGIC (REVISI ANTI-429) ---
    max_retries = 4
    for attempt in range(max_retries):
        try:
            # Timeout diperpanjang jadi 30 detik
            with requests.get(url, stream=True, timeout=30, headers=headers) as response:
                
                # JIKA SUKSES (200)
                if response.status_code == 200:
                    with open(path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk: f.write(chunk)
                    return (idx, path) 
                
                # JIKA KENA LIMIT (429) - TUNGGU LAMA
                elif response.status_code == 429:
                    wait_time = (attempt + 2) * 3  # Tunggu 3s, 6s, 9s, dst.
                    print(f"⚠️ Step {idx+1} kena limit (429). Santai dulu {wait_time} detik...")
                    time.sleep(wait_time)
                    continue # Coba lagi setelah tidur
                
                # ERROR LAIN
                else:
                    print(f"⚠️ Step {idx+1} gagal (Status: {response.status_code})")
        
        except requests.exceptions.RequestException as e:
            # Error koneksi internet biasa
            print(f"⚠️ Koneksi putus step {idx+1}: {e}")
            time.sleep(2)
            
        # Jeda acak antar percobaan agar tidak terdeteksi robot
        time.sleep(random.uniform(1, 3))
    
    print(f"❌ Gagal download step {idx+1} setelah {max_retries} kali coba.")
    return (idx, None)

def _run_background_download(queue):
    """
    Download background dilakukan SATU PER SATU (Sequential)
    agar tidak membebani server gratisan.
    """
    if not queue: return
    print(f"[BACKGROUND] 🚀 Memulai download sisa {len(queue)} gambar (Mode Santai)...")
    
    # Ubah max_workers jadi 1 agar antrian santai
    with ThreadPoolExecutor(max_workers=1) as executor:
        executor.map(_download_single_image, queue)
    print("[BACKGROUND] ✅ Semua gambar latar belakang selesai.")

def generate_and_save_images(dish_name, steps):
    print(f"\n[VISUALIZER] 🎨 Menyiapkan ilustrasi untuk '{dish_name}'...")
    
    # 1. Bersihkan Folder
    safe_name = "".join([c for c in dish_name if c.isalnum() or c in (' ','-')]).strip().replace(" ", "_")
    recipe_folder = os.path.join(IMAGE_DIR, safe_name)
    
    if os.path.exists(recipe_folder):
        try: shutil.rmtree(recipe_folder)
        except: pass
    if not os.path.exists(recipe_folder):
        os.makedirs(recipe_folder)

    # 2. Generate Prompt (Optimasi Token)
    steps_text = [s['instruction'][:100] for s in steps] # Ambil 100 huruf pertama saja per step
    prompt_gen = f"""
    Create visual prompts for cooking: "{dish_name}".
    Steps: {steps_text}
    Output JSON: {{ "prompts": ["string1", "string2"...] }}
    Prompts must be short (max 10 words), English, photorealistic style.
    Length match steps count.
    """
    
    try:
        res = model.generate_content(prompt_gen, generation_config=fast_config)
        prompts = json.loads(res.text).get('prompts', [])
    except:
        prompts = [f"Cooking {dish_name} step {i+1} close up photorealistic" for i in range(len(steps))]

    # Pastikan jumlah prompt sama dengan steps
    if len(prompts) < len(steps):
        prompts.extend([f"Cooking {dish_name} food photography"] * (len(steps) - len(prompts)))

    # 3. SPLIT DOWNLOAD
    # Kurangi prioritas download agar user cepat masuk UI
    # Misal Nasi Padang 15 step -> Priority cuma 2 gambar pertama saja.
    priority_count = 2 
    
    priority_tasks = []
    background_tasks = []
    final_paths = [None] * len(steps)
    
    for i, p in enumerate(prompts):
        file_path = os.path.join(recipe_folder, f"step_{i+1}.jpg")
        final_paths[i] = file_path # Simpan path harapan
        
        task = (p, file_path, i)
        if i < priority_count:
            priority_tasks.append(task)
        else:
            background_tasks.append(task)

    # 4. EKSEKUSI PRIORITY (Max Workers dikurangi jadi 2)
    if priority_tasks:
        print(f"[VISUALIZER] ⏳ Download {len(priority_tasks)} gambar utama...")
        with ThreadPoolExecutor(max_workers=2) as executor:
            list(executor.map(_download_single_image, priority_tasks))

    # 5. EKSEKUSI BACKGROUND
    if background_tasks:
        t = threading.Thread(target=_run_background_download, args=(background_tasks,))
        t.daemon = True 
        t.start()
        print(f"[VISUALIZER] ⏩ {len(background_tasks)} gambar sisa didownload di background.")

    return final_paths