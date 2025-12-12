import ollama
import json
import io
from PIL import Image

# Gunakan LLaVA agar lebih pintar logikanya (walau agak lambat)
# Kalau mau cepat ganti jadi "moondream", tapi LLaVA lebih akurat buat logic ini.
VISION_MODEL = "llava" 

CYAN = "\033[96m"
MAGENTA = "\033[95m"
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

def evaluate_cooking_step(image, instruction):
    print(f"{MAGENTA}[VISION AGENT] 👁️ Inspeksi Ketat Foto Masakan...{RESET}")
    
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
    
    # --- 2. PROMPT STRICT (TIDAK TOLERAN) ---
    # Kita minta AI membedakan 3 FASE: PREP (Persiapan), COOK (Masak), SERVE (Saji)
    
    prompt = f"""
    Act as a STRICT Cooking Inspector. Do NOT be lenient.
    
    Instruction: "{instruction}"
    
    TASK: Determine if the image matches the specific STAGE of cooking described.
    
    LOGIC CHECKS (STRICT):
    1. PHASE CHECK:
       - If instruction implies PREPARATION (cut, wash, mix, raw) -> Image MUST show raw food/cutting board/bowls.
       - If instruction implies COOKING (fry, boil, sauté, heat) -> Image MUST show a pan/pot, fire, oil, or steam.
       - If instruction implies SERVING (plate, garnish, eat) -> Image MUST show cooked food on a plate.
       
    2. MISMATCH RULES (AUTO-FAIL):
       - Instruction says "Fry/Cook" but image shows RAW food on cutting board -> FAIL.
       - Instruction says "Wash/Cut" but image shows COOKING in pan -> FAIL.
       - Instruction says "Serve" but image shows RAW food -> FAIL.
    
    Output strictly JSON:
    {{
        "status": "PASS" or "FAIL",
        "feedback": "Reason in Indonesian (max 10 words)"
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
        
        # Cari kurung kurawal JSON (jaga-jaga kalau ada teks sampah)
        start_idx = content.find('{')
        end_idx = content.rfind('}') + 1
        
        if start_idx != -1 and end_idx != -1:
            data = json.loads(content[start_idx:end_idx])
        else:
            # Kalau output rusak, kita anggap FAIL biar aman
            data = {"status": "FAIL", "feedback": "AI Gagal membaca gambar."}
        
        # Print hasil di terminal
        if data.get('status') == 'PASS':
            print(f"{GREEN}[VISION AGENT] ✅ PASS: {data.get('feedback')}{RESET}")
        else:
            print(f"{RED}[VISION AGENT] ❌ FAIL: {data.get('feedback')}{RESET}")
            
        return data
        
    except Exception as e:
        print(f"{RED}[VISION ERROR] {e}{RESET}")
        # Kalau error teknis, return FAIL biar user sadar ada yang salah
        return {"status": "FAIL", "feedback": "Error sistem visi."}