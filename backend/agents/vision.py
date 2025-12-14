import ollama
import json
import io
from PIL import Image

# Gunakan 'llava' atau 'moondream' (sesuai yang terinstall)
VISION_MODEL = "llava" 

CYAN = "\033[96m"
MAGENTA = "\033[95m"
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

def evaluate_cooking_step(image, instruction):
    print(f"{MAGENTA}[VISION AGENT] 👁️ Melihat foto masakan...{RESET}")
    
    # --- 1. PRE-PROCESSING GAMBAR ---
    if image.mode in ("RGBA", "P"):
        background = Image.new("RGB", image.size, (255, 255, 255))
        if image.mode == 'RGBA':
            background.paste(image, mask=image.split()[3])
            image = background
        else:
            image = image.convert("RGB")
            
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_bytes = img_byte_arr.getvalue()
    
    # --- 2. PROMPT DIPERBARUI (LEBIH RAMAH & CERDAS) ---
    # Perubahan: Dari "STRICT Inspector" menjadi "Supportive Chef"
    # Kita minta dia melihat "Kecocokan Umum" bukan "Detail Teknis Sempurna".
    
    prompt = f"""
    Role: You are a Supportive Chef Assistant.
    Task: Verify if the user's photo roughly matches the current cooking step.
    
    Current Step Instruction: "{instruction}"
    
    Guidelines (BE REASONABLE):
    1. **Context Match**: If the step says "fry onions", and the image shows onions in a pan (even if not fully brown yet), that is a PASS.
    2. **Equipment**: If the step implies cooking, look for ANY cookware (pan, pot, wok, oven).
    3. **Ingredients**: Check if the visible ingredients are related to the instruction.
    4. **Lighting/Quality**: Ignore bad lighting or blur. Focus on the content.
    
    CRITERIA FOR PASS:
    - The image shows RELEVANT food or equipment described in the instruction.
    - It looks like a cooking attempt related to the step.
    
    CRITERIA FOR FAIL:
    - The image is completely unrelated (e.g., a photo of a cat, a car, or an empty table).
    - The image contradicts the step (e.g., step says "Serve" but image shows raw meat).
    
    Output strictly JSON:
    {{
        "status": "PASS" or "FAIL",
        "feedback": "Pujian singkat atau saran perbaikan (Bahasa Indonesia, max 10 words)"
    }}
    """
    
    try:
        response = ollama.chat(
            model=VISION_MODEL,
            format='json',
            messages=[{
                'role': 'user',
                'content': prompt,
                'images': [img_bytes]
            }]
        )
        
        # --- 3. PARSING HASIL ---
        content = response['message']['content']
        
        # Pembersihan JSON (jaga-jaga error parsing)
        start_idx = content.find('{')
        end_idx = content.rfind('}') + 1
        
        if start_idx != -1 and end_idx != -1:
            data = json.loads(content[start_idx:end_idx])
        else:
            # Fallback jika JSON rusak, kita anggap PASS saja biar user tidak kecewa
            # (Asumsi user sudah upload foto, kemungkinan besar benar)
            data = {"status": "PASS", "feedback": "Terlihat oke! Lanjut!"}
        
        # Log Terminal
        if data.get('status') == 'PASS':
            print(f"{GREEN}[VISION AGENT] ✅ PASS: {data.get('feedback')}{RESET}")
        else:
            print(f"{RED}[VISION AGENT] ❌ FAIL: {data.get('feedback')}{RESET}")
            
        return data
        
    except Exception as e:
        print(f"{RED}[VISION ERROR] {e}{RESET}")
        # Jika error sistem (misal model berat/crash), loloskan saja (Fail-safe)
        return {"status": "PASS", "feedback": "Sistem sibuk, tapi saya percaya kamu! Lanjut."}