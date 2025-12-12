import streamlit as st
from PIL import Image
import time
from frontend.components import render_ingredient_card, render_nutrition_card, render_step_card, render_shopping_card, render_chat_message
from backend.agents.vision import evaluate_cooking_step
from backend.agents.consultant import ask_chef_consultant

# --- FUNGSI POPUP (DIALOG) SELESAI ---
@st.dialog("🎉 Masakan Selesai!")
def show_finish_dialog():
    st.markdown("### 🥳 Hore! Kamu Hebat Chef!")
    st.write("Kamu telah menyelesaikan semua langkah resep ini dengan sempurna.")
    st.write("Jangan lupa foto hasil akhirnya dan nikmati makanannya! 🍽️")
    st.balloons()
    
    # Tombol Reset
    if st.button("🏠 Kembali ke Menu Utama", type="primary", use_container_width=True):
        # Reset Semua State
        st.session_state.recipe = None
        st.session_state.messages = [{"role": "assistant", "content": "Halo! ChefBot siap bantu. Mau masak apa lagi sekarang?"}]
        st.session_state.step_index = 0
        st.session_state.nutrition = None
        st.session_state.shopping = None
        st.rerun()

def render_cooking_view():
    recipe = st.session_state.recipe
    idx = st.session_state.step_index
    total = len(recipe['steps'])
    
    # --- CEK SELESAI ---
    # Jika index langkah sudah melebihi jumlah langkah, tampilkan Popup
    if idx >= total:
        show_finish_dialog()
        return # Stop render agar tidak error index

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
        
        # --- UPLOAD & VISION (DIPERBARUI) ---
        with st.expander("📸 UPLOAD BUKTI MASAK (Opsional)", expanded=True):
            uploaded_file = st.file_uploader("Kirim foto untuk dinilai Juri AI:", type=["jpg","png"], key=f"up_{idx}")
            
            if uploaded_file:
                image = Image.open(uploaded_file)
                st.image(image, width=250)
            
            st.write("")
            
            # --- DUA TOMBOL: NILAI vs LEWATI ---
            btn_col1, btn_col2 = st.columns(2)
            
            with btn_col1:
                # Tombol Juri AI
                if st.button("🔍 Nilai Masakan", type="primary", use_container_width=True):
                    if not uploaded_file:
                        st.warning("Upload foto dulu dong Chef! 📸")
                    else:
                        with st.spinner("Juri sedang mencicipi..."):
                            res = evaluate_cooking_step(image, instruction)
                        
                        if res['status'] == 'PASS':
                            st.success(f"✅ {res['feedback']}")
                            time.sleep(1)
                            st.session_state.step_index += 1
                            st.rerun()
                        else:
                            st.error(f"❌ {res['feedback']}")
            
            with btn_col2:
                # Tombol Skip (Jalan Pintas)
                if st.button("⏩ Lewati Langkah", use_container_width=True):
                    st.info("Langkah dilewati! (Juri tutup mata 🙈)")
                    time.sleep(0.5)
                    st.session_state.step_index += 1
                    st.rerun()

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

    # Tombol Darurat Reset
    if st.button("🔄 Batal Masak / Reset", use_container_width=True):
        st.session_state.recipe = None
        st.session_state.messages = []
        st.rerun()