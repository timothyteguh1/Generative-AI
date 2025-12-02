import streamlit as st
from PIL import Image
import time

# --- IMPORTS ---
from config import configure_ai, setup_folders
from frontend.styles import load_css
from frontend.components import render_header, render_chat_message, render_ingredient_card, render_nutrition_card, render_step_card , render_shopping_card
from backend.data_manager import save_recipe

# Import Agents
try:
    from backend.agents.planner import generate_recipe_plan
    from backend.agents.nutritionist import analyze_nutrition
    from backend.agents.vision import evaluate_cooking_step
    from backend.agents.consultant import ask_chef_consultant
    from backend.agents.shopper import generate_shopping_list
except ImportError:
    st.error("⚠️ Folder backend/agents belum lengkap.")
    st.stop()

# --- SETUP ---
st.set_page_config(page_title="ChefBot Pro", page_icon="👨‍🍳", layout="wide", initial_sidebar_state="collapsed")
configure_ai()
setup_folders()
load_css() # Load CSS Fix

# --- STATE ---
if "recipe" not in st.session_state:
    st.session_state.recipe = None
    st.session_state.nutrition = None
    st.session_state.step_index = 0
    st.session_state.shopping = None
    st.session_state.messages = [{"role": "assistant", "content": "Halo! ChefBot siap bantu. Mau masak apa hari ini?"}]

# --- HEADER ---
render_header()

# ============================
# MODE 1: CHAT / INPUT AWAL
# ============================
if not st.session_state.recipe:
    # Area Chat (Scrollable)
    with st.container():
        for msg in st.session_state.messages:
            render_chat_message(msg["role"], msg["content"])
    
    st.write("") # Spacer

    # Input di Bawah
    user_input = st.chat_input("Ketik masakan... (Contoh: Ayam Goreng Lengkuas)")
    
    if user_input:
        # Tampilkan chat user
        st.session_state.messages.append({"role": "user", "content": user_input})
        render_chat_message("user", user_input)
        
        # Proses Agent
        with st.spinner("🔥 Chef sedang meracik resep..."):
            recipe_data = generate_recipe_plan(user_input)
            
        if recipe_data:
            with st.spinner("🍎 Menghitung gizi..."):
                nutri_data = analyze_nutrition(recipe_data)
            with st.spinner("🛒 Mencari bahan belanja..."):
                shopping_data = generate_shopping_list(recipe_data['ingredients'])
                st.session_state.shopping = shopping_data
                
            with st.spinner("💾 Menyimpan resep..."):
                save_recipe(recipe_data) # Simpan Data
            
            st.session_state.recipe = recipe_data
            st.session_state.nutrition = nutri_data
            st.session_state.step_index = 0
            st.session_state.messages = [] # Reset chat lama
            st.rerun()

# ============================
# MODE 2: DASHBOARD MASAK
# ============================
elif st.session_state.recipe:
    recipe = st.session_state.recipe
    idx = st.session_state.step_index
    total = len(recipe['steps'])
    
    # Data Langkah
    step_data = recipe['steps'][idx]
    instruction = step_data.get('instruction', str(step_data)) if isinstance(step_data, dict) else str(step_data)
    visual_key = step_data.get('visual_keyword', 'cooking') if isinstance(step_data, dict) else 'cooking'

    st.markdown(f"<h3 style='text-align:center; color:#D35400;'>🍽️ {recipe['dish']}</h3>", unsafe_allow_html=True)

    # Layout 2 Kolom
    col1, col2 = st.columns([1, 2], gap="large")

    # KOLOM KIRI
    with col1:
        render_ingredient_card(recipe['ingredients'])
        render_nutrition_card(st.session_state.nutrition)
        st.write("") # Spacer dikit
        render_shopping_card(st.session_state.shopping)

    # KOLOM KANAN
    with col2:
        st.progress(int(((idx + 1) / total) * 100))
        
        # Tampilkan Gambar & Langkah
        render_step_card(idx, total, instruction, visual_key)
        
        st.write("")
        
        # Upload Box (Vision)
        with st.expander("📸 UPLOAD BUKTI MASAK", expanded=True):
            uploaded_file = st.file_uploader("Kirim foto:", type=["jpg","png"], key=f"up_{idx}")
            
            if uploaded_file:
                image = Image.open(uploaded_file)
                st.image(image, width=250)
                
                if st.button("🔍 Nilai Masakan", type="primary", use_container_width=True):
                    with st.spinner("Juri menilai..."):
                        res = evaluate_cooking_step(image, instruction)
                    
                    if res['status'] == 'PASS':
                        st.success(f"✅ {res['feedback']}")
                        time.sleep(2)
                        st.session_state.step_index += 1
                        if st.session_state.step_index >= total:
                            st.balloons()
                            st.session_state.recipe = None
                        st.rerun()
                    else:
                        st.error(f"❌ {res['feedback']}")

    # --- AREA CHAT KONSULTASI ---
    st.markdown("---")
    st.caption("💬 Tanya Chef tentang langkah ini:")
    
    with st.container(height=200):
        for msg in st.session_state.messages:
            render_chat_message(msg["role"], msg["content"])

    user_q = st.chat_input(f"Bingung langkah {idx+1}? Tanya di sini...")
    if user_q:
        st.session_state.messages.append({"role": "user", "content": user_q})
        with st.spinner("..."):
            ans = ask_chef_consultant(user_q, recipe['dish'], instruction)
        st.session_state.messages.append({"role": "assistant", "content": ans})
        st.rerun()

    if st.button("🔄 Reset Resep", use_container_width=True):
        st.session_state.recipe = None
        st.session_state.messages = []
        st.rerun()