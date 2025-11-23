import google.generativeai as genai
import json
import streamlit as st
from config import configure_ai

# Setup
configure_ai()

# --- KITA PAKAI MODEL TERBARU DARI DAFTARMU ---
# Gemini 2.5 Flash sangat jago melihat gambar
model = genai.GenerativeModel('models/gemini-2.5-flash')

def evaluate_cooking_step(image, current_instruction):
    print(f"\n👁️ [VISION] Melihat gambar dengan Gemini 2.5...")
    
    prompt = f"""
    Kamu Juri Masak. Instruksi: "{current_instruction}".
    Lihat gambar. Sesuai?
    Jawab HANYA JSON murni (tanpa ```json).
    Format: {{ "status": "PASS" atau "FAIL", "feedback": "Alasan singkat" }}
    """
    
    try:
        # Input list [prompt, image]
        response = model.generate_content([prompt, image])
        print("✅ [VISION] Selesai!")
        
        text_bersih = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(text_bersih)
        
    except Exception as e:
        print(f"❌ [VISION ERROR] {e}")
        return {"status": "FAIL", "feedback": "Maaf, mata saya error. Coba foto lagi."}