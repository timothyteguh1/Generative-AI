import urllib.parse
import random

# Visualizer sekarang fokus hanya pada HASIL AKHIR
def generate_final_dish_image(dish_name):
    print(f"\n[VISUALIZER] 🎨 Menggambar hasil akhir: {dish_name}...")
    
    # Prompt khusus untuk Food Photography hasil jadi
    # Kita buat sangat detail agar hasilnya menggugah selera
    base_prompt = (
        f"Professional food photo of {dish_name}, final dish, "
        f"restaurant plating, bokeh background, garnished perfectly, "
        f"hyper-realistic, 8k, cinematic lighting, food photography, "
        f"sharp focus, f/1.8 aperture, delicious looking"
    )
    
    safe_prompt = urllib.parse.quote(base_prompt)
    seed = random.randint(100, 99999)
    
    # Generate 1 URL saja menggunakan model Flux (kualitas tinggi)
    url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=1024&height=768&model=flux&nologo=true&seed={seed}"
    
    print(f"✅ Final Image URL: {url[:50]}...")
    return url