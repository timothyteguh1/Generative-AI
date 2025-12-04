import streamlit as st
from frontend.components import render_chat_message
from backend.agents.planner import generate_recipe_plan
from backend.agents.visualizer import generate_and_save_images
from backend.agents.nutritionist import analyze_nutrition
from backend.agents.shopper import generate_shopping_list
from backend.data_manager import save_recipe

def render_home_view():
    # Tampilkan History Chat
    for msg in st.session_state.messages:
        render_chat_message(msg["role"], msg["content"])
    
    st.write("")
    
    # Input User
    user_input = st.chat_input("Ketik masakan... (Contoh: Ayam Goreng Lengkuas)")
    
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        render_chat_message("user", user_input)
        
        # --- PROSES AI ---
        with st.spinner("🔥 Chef sedang meracik resep..."):
            recipe_data = generate_recipe_plan(user_input)
        
        if recipe_data:
            # 1. Download Gambar (Visualizer)
            with st.spinner("🎨 Menggambar ilustrasi langkah..."):
                image_paths = generate_and_save_images(recipe_data['dish'], recipe_data['steps'])
                for i, step in enumerate(recipe_data['steps']):
                    step['image_path'] = image_paths[i]
            
            # 2. Hitung Gizi & Belanja
            with st.spinner("🍎 Menghitung gizi & 🛒 Mencari bahan..."):
                nutri_data = analyze_nutrition(recipe_data)
                shopping_data = generate_shopping_list(recipe_data['ingredients'])
            
            # 3. Simpan State
            st.session_state.shopping = shopping_data
            save_recipe(recipe_data)
            
            st.session_state.recipe = recipe_data
            st.session_state.nutrition = nutri_data
            st.session_state.step_index = 0
            st.session_state.messages = [] 
            st.rerun()