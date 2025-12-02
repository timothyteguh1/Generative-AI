import google.generativeai as genai
import json
import urllib.parse
from config import configure_ai

configure_ai()
model = genai.GenerativeModel('models/gemini-2.5-flash')

# --- WARNA TERMINAL ---
CYAN = "\033[96m"
RESET = "\033[0m"


def generate_shopping_list(ingredients):
    # [LOG]
    print(f"{CYAN}[SHOPPER AGENT] 🛒 Mencari toko online untuk bahan-bahan...{RESET}")

    # Kita minta AI untuk mengategorikan bahan (misal: Sayur, Daging, Bumbu)
    # Dan kita buat link search manual di python nanti agar lebih akurat
    prompt = f"""
    Dari daftar bahan ini: {ingredients}, 
    Kelompokkan menjadi JSON kategori sederhana:
    {{
        "items": [
            {{"name": "Nama Bahan (misal: Dada Ayam)", "category": "Daging"}},
            {{"name": "Nama Bahan (misal: Bawang Putih)", "category": "Bumbu"}}
        ]
    }}
    Hanya sertakan bahan utama yang perlu dibeli.
    """
    
    try:
        res = model.generate_content(prompt)
        text = res.text.replace("```json","").replace("```","").strip()
        s = text.find('{'); e = text.rfind('}')
        data = json.loads(text[s:e+1])
        
        # Tambahkan Link Belanja Otomatis (Tokopedia & Shopee)
        final_list = []
        for item in data.get('items', []):
            query = urllib.parse.quote(item['name'])
            item['link_toped'] = f"https://www.tokopedia.com/search?st=product&q={query}"
            item['link_shopee'] = f"https://shopee.co.id/search?keyword={query}"
            final_list.append(item)
            
        print(f"{CYAN}[SHOPPER AGENT] ✅ Link belanja siap!{RESET}")
        return final_list
    except Exception as e:
        print(f"\033[91m[SHOPPER AGENT] ❌ Error: {e}{RESET}")
        return []