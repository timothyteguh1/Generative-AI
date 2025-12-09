import google.generativeai as genai
import json
import urllib.parse
from config import configure_ai

configure_ai()

# Model Otak (Teks) untuk merancang adegan foto
try:
    text_model = genai.GenerativeModel('models/gemini-2.5-flash')
except:
    text_model = genai.GenerativeModel('models/gemini-1.5-flash')

# Config agar respon cepat dan terstruktur
fast_config = genai.types.GenerationConfig(
    temperature=0.3, response_mime_type="application/json"
)

def generate_and_save_images(dish_name, steps):
    print(f"\n[VISUALIZER] 🔗 Merancang Prompt Visual untuk '{dish_name}'...")
    
    # 1. OPTIMASI PROMPT (Agar gambar sesuai & estetik)
    steps_text = [s['instruction'] for s in steps]
    
    # Kita minta Gemini jadi "Art Director"
    prompt_gen = f"""
    Act as a professional Food Photographer Art Director.
    Create concise but highly descriptive visual prompts for cooking steps: "{dish_name}".
    
    Context Steps: {steps_text}
    
    Output STRICT JSON: {{ "prompts": ["string1", "string2"...] }}
    
    RULES FOR PROMPTS:
    1. MUST be in English.
    2. Focus on the ACTION (e.g., "Close up shot of slicing onions", "Boiling soup in a pot").
    3. Style keywords to append: "Hyper-realistic, 8k resolution, cinematic lighting, macro food photography, sharp focus, steam rising, delicious texture".
    4. Keep it under 25 words per prompt for faster generation.
    5. Exact length match with steps count.
    """
    
    try:
        # Generate deskripsi gambar
        res = text_model.generate_content(prompt_gen, generation_config=fast_config)
        prompts = json.loads(res.text).get('prompts', [])
    except:
        # Fallback jika gagal
        prompts = [f"Cooking {dish_name} step {i+1} hyperrealistic food photo" for i in range(len(steps))]

    # Validasi panjang list
    if len(prompts) < len(steps):
        prompts.extend([f"Cooking {dish_name}"] * (len(steps) - len(prompts)))

    # 2. GENERATE URL (Optimasi Speed)
    image_urls = []
    
    for i, p in enumerate(prompts):
        # Encode URL
        safe_prompt = urllib.parse.quote(p)
        
        # Seed acak agar gambar tidak monoton
        seed = len(p) + i + 555
        
        # --- SETTING OPTIMAL ---
        # 1. Model: 'flux' (Paling bagus saat ini di Pollinations)
        # 2. Ukuran: 512x384 (Lebih kecil = Loading browser lebih cepat)
        # 3. Nologo: True (Bersih)
        url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=512&height=384&model=flux&nologo=true&seed={seed}"
        
        image_urls.append(url)
        print(f"✅ Link Visual Step {i+1} siap: {p[:30]}...")

    return image_urls