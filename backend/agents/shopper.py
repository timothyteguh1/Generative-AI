import google.generativeai as genai
import json
import urllib.parse
import re  # <--- TAMBAHKAN INI
from config import configure_ai

configure_ai()
model = genai.GenerativeModel('models/gemini-2.5-flash')

# --- WARNA TERMINAL ---
CYAN = "\033[96m"
RESET = "\033[0m"

def generate_shopping_list(ingredients):
    # [LOG]
    print(f"{CYAN}[SHOPPER AGENT] 🛒 Mencari toko online untuk bahan-bahan...{RESET}")

    prompt = f"""
    Dari daftar bahan ini: {ingredients}, 
    Kelompokkan menjadi JSON kategori sederhana:
    {{
        "items": [
            {{"name": "Nama Bahan Lengkap", "category": "Daging"}},
            {{"name": "Nama Bahan Lengkap", "category": "Bumbu"}}
        ]
    }}
    Hanya sertakan bahan utama yang perlu dibeli.
    """
    
    try:
        res = model.generate_content(prompt)
        text = res.text.replace("```json","").replace("```","").strip()
        s = text.find('{'); e = text.rfind('}')
        data = json.loads(text[s:e+1])
        
        final_list = []
        for item in data.get('items', []):
            original_name = item['name']
            
            # --- LOGIKA PEMBERSIHAN NAMA (REGEX) ---
            # Menghapus teks di dalam kurung (...) beserta spasi sebelumnya
            clean_name = re.sub(r'\s*\(.*?\)', '', original_name).strip()
            
            # Update nama di dictionary agar bersih saat ditampilkan
            item['name'] = clean_name
            
            # Buat link berdasarkan nama yang sudah bersih
            query = urllib.parse.quote(clean_name)
            item['link_toped'] = f"https://www.tokopedia.com/search?st=product&q={query}"
            item['link_shopee'] = f"https://shopee.co.id/search?keyword={query}"
            final_list.append(item)
            
        print(f"{CYAN}[SHOPPER AGENT] ✅ Link belanja siap!{RESET}")
        return final_list
    except Exception as e:
        print(f"\033[91m[SHOPPER AGENT] ❌ Error: {e}{RESET}")
        return []