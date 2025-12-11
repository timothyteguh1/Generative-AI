import ollama
import json
import io
from PIL import Image

# Pastikan model llava sudah di-pull: ollama pull llava
VISION_MODEL = "moondream"

CYAN = "\033[96m"
MAGENTA = "\033[95m"
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

def evaluate_cooking_step(image, instruction):
    print(f"{MAGENTA}[VISION AGENT] 👁️ Menganalisis foto masakan dengan LLaVA (Mode Santai)...{RESET}")
    
    # --- 1. PRE-PROCESSING GAMBAR (PENTING) ---
    # Ubah RGBA (Transparan) ke RGB (Putih) agar tidak Error dan AI tidak bingung
    if image.mode in ("RGBA", "P"):
        background = Image.new("RGB", image.size, (255, 255, 255))
        if image.mode == 'RGBA':
            background.paste(image, mask=image.split()[3]) # 3 is the alpha channel
            image = background
        else:
            image = image.convert("RGB")
    
    # Konversi ke Bytes untuk dikirim ke Ollama
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_bytes = img_byte_arr.getvalue()
    
    # --- 2. PROMPT YANG LEBIH TOLERAN (LENIENT) ---
    # Perubahan Kunci:
    # - "Do not be strict" (Jangan kaku)
    # - "Focus on key elements" (Fokus pada bahan/alat utama saja)
    # - "Ignore style/lighting/background" (Abaikan gaya foto/background checkerboard)
    
    prompt = f"""
    You are a helpful cooking assistant verifying user photos.
    Instruction: "{instruction}"
    
    Task: Check if the image shows the MAIN INGREDIENTS or ACTION described in the instruction.
    
    RULES FOR JUDGING:
    1. Be LENIENT and FORGIVING. Do not be strict.
    2. Ignore image style, lighting, or background (e.g. checkerboard/transparent background is OK).
    3. If you see the main object (e.g., pan, oil, specific veggie) mentioned in instruction, output "PASS".
    4. Only output "FAIL" if the image is COMPLETELY unrelated (e.g., a photo of a cat for a cooking step).
    
    Output strictly JSON:
    {{
        "status": "PASS" or "FAIL",
        "feedback": "Short encouraging feedback in Indonesian (max 10 words)"
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
        
        # Parse JSON output
        content = response['message']['content']
        # Kadang LLaVA memberikan teks sebelum JSON, kita cari kurung kurawal
        start_idx = content.find('{')
        end_idx = content.rfind('}') + 1
        if start_idx != -1 and end_idx != -1:
            data = json.loads(content[start_idx:end_idx])
        else:
            # Fallback jika JSON rusak tapi respon ada
            data = {"status": "PASS", "feedback": "Terlihat oke, lanjut!"}
        
        if data.get('status') == 'PASS':
            print(f"{GREEN}[VISION AGENT] ✅ PASS: {data.get('feedback')}{RESET}")
        else:
            print(f"{RED}[VISION AGENT] ❌ FAIL: {data.get('feedback')}{RESET}")
            
        return data
        
    except Exception as e:
        print(f"{RED}[VISION ERROR] {e}{RESET}")
        # Default PASS jika error teknis, agar user tidak frustasi
        return {"status": "PASS", "feedback": "AI bingung, tapi lanjut aja!"}