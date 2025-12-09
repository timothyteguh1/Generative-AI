import streamlit as st
from PIL import Image
import time
from frontend.components import render_ingredient_card, render_nutrition_card, render_step_card, render_shopping_card, render_chat_message
from backend.agents.vision import evaluate_cooking_step
from backend.agents.consultant import ask_chef_consultant

def render_cooking_view():
    recipe = st.session_state.recipe
    idx = st.session_state.step_index
    total = len(recipe['steps'])
    step_data = recipe['steps'][idx]
    instruction = step_data.get('instruction', str(step_data))
    current_img_path = step_data.get('image_path', None)

    # --- JUDUL ---
    st.markdown(f"<h3 style='text-align:center; color:#D35400;'>🍽️ {recipe['dish']}</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2], gap="large")

    # --- KOLOM KIRI (INFO) ---
    with col1:
        render_ingredient_card(recipe['ingredients'])
        render_nutrition_card(st.session_state.nutrition)
        st.write("")
        render_shopping_card(st.session_state.shopping)

    # --- KOLOM KANAN (LANGKAH) ---
    with col2:
        st.progress(int(((idx + 1) / total) * 100))
        render_step_card(idx, total, instruction, current_img_path)
        
        st.write("")
        
        # --- UPLOAD & VISION ---
        with st.expander("📸 UPLOAD BUKTI MASAK", expanded=True):
            uploaded_file = st.file_uploader("Kirim foto:", type=["jpg","png"], key=f"up_{idx}")
            
            if uploaded_file:
                image = Image.open(uploaded_file)
                st.image(image, width=250)
                
                if st.button("🔍 Nilai Masakan", type="primary", use_container_width=True):
                    with st.spinner("Juri menilai..."):
                        # Panggil Vision Agent yang sudah diperbaiki
                        res = evaluate_cooking_step(image, instruction)
                    
                    if res['status'] == 'PASS':
                        st.success(f"✅ {res['feedback']}")
                        time.sleep(2)
                        st.session_state.step_index += 1
                        if st.session_state.step_index >= total:
                            st.balloons()
                            st.session_state.recipe = None
                            st.rerun()
                        st.rerun()
                    else:
                        st.error(f"❌ {res['feedback']}")

    # --- CHAT CONSULTANT ---
    st.markdown("""
        <p style='color: #2C3E50; font-size: 0.9rem; font-weight: 600; margin-bottom: 5px;'>
            💬 Tanya Chef tentang langkah ini:
        </p>
    """, unsafe_allow_html=True)
    
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

    if st.button("🔄 Reset Resep / Masak Ulang", use_container_width=True):
        st.session_state.recipe = None
        st.session_state.messages = []
        st.rerun()