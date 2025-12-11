import ollama
import json
import urllib.parse
import random

# Model ringan
MODEL_NAME = "llama3"

def generate_and_save_images(dish_name, steps):
    print(f"\n[VISUALIZER] 🔗 Merancang Prompt Visual dengan Ollama...")
    
    steps_text = [s['instruction'] for s in steps]
    total_steps = len(steps)
    
    # 1. Minta AI ambil Inti Aksi saja (tanpa embel-embel)
    prompt_gen = f"""
    Task: Extract the MAIN PHYSICAL ACTION from these cooking steps (max 4 words per step).
    Example: "Slicing onions", "Boiling water", "Frying chicken".
    
    Steps: {steps_text}
    
    Output STRICT JSON: {{ "prompts": ["action1", "action2"...] }}
    """
    
    try:
        response = ollama.chat(
            model=MODEL_NAME,
            format='json',
            messages=[{'role': 'user', 'content': prompt_gen}]
        )
        prompts = json.loads(response['message']['content']).get('prompts', [])
    except:
        prompts = [f"Cooking step {i+1}" for i in range(total_steps)]

    if len(prompts) < total_steps:
        prompts.extend([f"Step {i+1}"] * (total_steps - len(prompts)))

    image_urls = []
    
    # Style Dasar
    BASE_STYLE = "hyper-realistic, 8k, cinematic lighting, photorealistic, sharp focus"
    
    # 2. LOGIKA PENGECEKAN LANGKAH (Step Checking Logic)
    for i, action in enumerate(prompts):
        step_num = i + 1
        
        # --- LOGIKA PEMBAGIAN ZONA ---
        
        # A. ZONA PERSIAPAN (25% Langkah Pertama)
        # Fokus: Bahan Mentah, Pisau, Talenan.
        # DILARANG: Muncul nama masakan matang.
        if step_num <= total_steps * 0.25:
            context = "raw ingredients, kitchen preparation, uncooked, on cutting board"
            # Jangan masukkan 'dish_name' di sini agar tidak spoiler!
            full_prompt = f"{action}, {context}, {BASE_STYLE}"

        # B. ZONA PENYAJIAN (Langkah Terakhir)
        # Fokus: Makanan Jadi, Piring Cantik.
        # WAJIB: Muncul nama masakan.
        elif step_num == total_steps:
            context = f"final dish {dish_name}, garnished, beautiful plating, ready to serve"
            full_prompt = f"{action}, {context}, {BASE_STYLE}"
            
        # C. ZONA MEMASAK (Sisanya / Tengah-tengah)
        # Fokus: Wajan, Panci, Api, Uap.
        # BOLEH: Nama masakan tapi dalam konteks 'cooking'.
        else:
            context = f"cooking process, sizzling in pan/pot, steam rising, kitchen stove"
            # Kita sebut 'cooking {dish_name}' biar tidak jadi Pasta, 
            # tapi tambah 'close-up texture' biar fokus ke tekstur bukan plating.
            full_prompt = f"{action}, cooking {dish_name}, close-up food texture, {context}, {BASE_STYLE}"
        
        # 3. Generate URL
        safe_prompt = urllib.parse.quote(full_prompt)
        seed = random.randint(100, 99999)
        url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=512&height=384&model=flux&nologo=true&seed={seed}"
        
        image_urls.append(url)
        print(f"✅ Step {step_num} ({'PREP' if step_num <= total_steps*0.25 else 'COOK/SERVE'}): {action}...")

    return image_urls