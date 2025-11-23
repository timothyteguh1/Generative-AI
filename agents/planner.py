import google.generativeai as genai
import json
import streamlit as st
import re # Kita butuh Regex untuk mencari pola JSON
from config import configure_ai

# Setup
configure_ai()

# Gunakan model yang tersedia (Gemini 2.5 Flash)
try:
    model = genai.GenerativeModel('models/gemini-2.5-flash')
except:
    # Fallback ke Pro jika Flash error
    model = genai.GenerativeModel('models/gemini-pro')

def clean_json_text(text):
    """
    Fungsi Cerdas untuk mencari JSON di dalam teks sampah.
    Dia akan mencari kurung kurawal pertama { dan terakhir }.
    """
    try:
        # 1. Cari posisi kurung kurawal pertama '{'
        start_index = text.find('{')
        # 2. Cari posisi kurung kurawal terakhir '}'
        end_index = text.rfind('}')
        
        if start_index != -1 and end_index != -1:
            # Ambil teks hanya yang ada di dalam kurung itu
            json_str = text[start_index : end_index + 1]
            return json_str
        return text # Kembalikan aslinya jika tidak ketemu (biar error di log)
    except Exception:
        return text

def generate_recipe_plan(dish_name):
    print(f"\n🚀 [PLANNER] Request: {dish_name}")
    
    # Prompt dipertegas agar Gemini patuh
    prompt = f"""
    Kamu adalah Chef Profesional sistem. User ingin masak: {dish_name}.
    
    TUGAS: Buat resep dalam format JSON.
    BAHASA: Indonesia.
    
    ATURAN KERAS:
    1. HANYA output JSON. JANGAN ada kata pengantar seperti "Tentu", "Ini resepnya".
    2. JANGAN gunakan Markdown (```json).
    3. Pastikan format JSON valid (ada koma antar item).
    
    STRUKTUR JSON:
    {{
        "dish": "Nama Masakan (judul menarik)",
        "ingredients": [
            "Bahan 1 (jumlah)",
            "Bahan 2 (jumlah)"
        ],
        "steps": [
            "Langkah 1: Siapkan...",
            "Langkah 2: Tumis...",
            "Langkah 3: Sajikan..."
        ]
    }}
    """
    
    try:
        print(f"⏳ [PLANNER] Menghubungi AI...")
        response = model.generate_content(prompt)
        
        # --- BAGIAN PEMBERSIH ---
        raw_text = response.text
        clean_text = clean_json_text(raw_text)
        
        print("✅ [PLANNER] Berhasil parsing JSON!")
        return json.loads(clean_text)
        
    except Exception as e:
        print(f"❌ [PLANNER ERROR] {e}")
        print(f"📄 [DATA MENTAH]: {response.text if 'response' in locals() else 'No Response'}")
        
        st.error(f"Maaf, Chef agak pusing membaca resepnya. Coba ulangi lagi ya. (Error: {e})")
        return None