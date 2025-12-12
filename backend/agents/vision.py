import ollama
import io
from PIL import Image

# Gunakan model vision ringan
VISION_MODEL = "moondream" 

CYAN = "\033[96m"
MAGENTA = "\033[95m"
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

def evaluate_cooking_step(image, instruction):
    print(f"{MAGENTA}[VISION AGENT] 👁️ Melihat foto user (Mode Teks Sederhana)...{RESET}")
    
    # 1. Pre-process Gambar (Wajib utk cegah error RGBA)
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
    
    # 2. Prompt yang TIDAK Minta JSON (Lebih Aman utk Model Kecil)
    prompt = f"""
    Instruction: "{instruction}"
    Look at the image. Does it match the instruction?
    
    Rules:
    1. Be LENIENT. If you see the main ingredients (like potatoes, water, ice), say YES.
    2. Only say NO if the image is completely wrong (like a cat or a car).
    
    OUTPUT FORMAT:
    Start your answer with "YES" or "NO", followed by a comma, then a very short reason (Indonesian).
    Example: YES, terlihat ada potongan kentang.
    """
    
    try:
        response = ollama.chat(
            model=VISION_MODEL,
            messages=[{
                'role': 'user',
                'content': prompt,
                'images': [img_bytes]
            }]
        )
        
        # 3. Parsing Manual (Lebih Stabil daripada JSON)
        raw_answer = response['message']['content'].strip()
        print(f"[DEBUG AI RAW]: {raw_answer}") # Cek apa kata AI sebenarnya di terminal
        
        # Ambil kata pertama (YES/NO)
        if raw_answer.upper().startswith("YES"):
            status = "PASS"
            # Ambil sisa kalimat setelah koma sebagai feedback
            parts = raw_answer.split(',', 1)
            feedback = parts[1].strip() if len(parts) > 1 else "Bagus, sesuai!"
            print(f"{GREEN}[VISION AGENT] ✅ PASS: {feedback}{RESET}")
            
        elif raw_answer.upper().startswith("NO"):
            status = "FAIL"
            parts = raw_answer.split(',', 1)
            feedback = parts[1].strip() if len(parts) > 1 else "Tidak sesuai instruksi."
            print(f"{RED}[VISION AGENT] ❌ FAIL: {feedback}{RESET}")
            
        else:
            # Jika AI ngelantur ga jelas, anggap PASS aja
            status = "PASS"
            feedback = "Terlihat oke."
            print(f"{GREEN}[VISION AGENT] ⚠️ AI Ragu, auto-pass.{RESET}")

        return {"status": status, "feedback": feedback}
        
    except Exception as e:
        print(f"{RED}[VISION ERROR] {e}{RESET}")
        return {"status": "PASS", "feedback": "Sistem error, lanjut saja."}