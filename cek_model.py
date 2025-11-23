import google.generativeai as genai
from config import configure_ai

# Setup API Key
configure_ai()

print("\n🔍 SEDANG MENCARI MODEL YANG TERSEDIA DI AKUNMU...")
print("="*50)

try:
    # Minta daftar model ke Google
    found = False
    for m in genai.list_models():
        # Kita cari model yang bisa generate text (generateContent)
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ DITEMUKAN: {m.name}")
            found = True
            
    if not found:
        print("❌ Tidak ada model yang cocok ditemukan.")
        
except Exception as e:
    print(f"❌ ERROR: {e}")

print("="*50)