import streamlit as st
from PIL import Image
import time
import textwrap 
from frontend.components import render_ingredient_card, render_nutrition_card, render_step_card, render_shopping_card, render_chat_message
from backend.agents.vision import evaluate_cooking_step
from backend.agents.consultant import ask_chef_consultant

# --- FUNGSI POPUP (DIALOG) DENGAN LOADING SCENE ---
@st.dialog("🎉 Masakan Selesai!", width="large")
def show_finish_dialog(image_url=None, dish_name=""):
    st.markdown(f"### 🥳 Hore! {dish_name} Siap Disajikan!")
    
    # Container Kosong untuk Animasi Loading / Gambar
    visual_container = st.empty()
    
    # 1. TAMPILKAN LOADING SCENE DULU
    loading_html = textwrap.dedent("""
        <div style="
            text-align: center; 
            padding: 40px 20px; 
            background-color: #FFF3E0; 
            border: 2px dashed #D35400; 
            border-radius: 15px; 
            margin-bottom: 20px;
        ">
            <div style="font-size: 4rem; margin-bottom: 10px; animation: bounce 1s infinite;">👨‍🍳</div>
            <h3 style="color: #D35400; margin: 0; font-family: sans-serif;">Chef sedang menata piring...</h3>
            <p style="color: #888; margin-top: 5px; font-size: 0.9rem;">Memberikan sentuhan terakhir ✨</p>
        </div>
    """)
    visual_container.markdown(loading_html, unsafe_allow_html=True)
    
    # 2. SIMULASI DELAY
    time.sleep(2.0)
    
    # 3. BERSIHKAN LOADING & TAMPILKAN GAMBAR
    visual_container.empty()
    
    if image_url:
        # Tampilkan Gambar Final
        st.image(
            image_url, 
            use_container_width=True, 
            caption=f"✨ Hasil Karya: {dish_name}"
        )
    else:
        # Fallback Jika Gambar Gagal
        fallback_html = textwrap.dedent(f"""
        <div style="text-align: center; padding: 40px; background: #F5F5F5; border-radius: 12px; color: #888;">
            <div style="font-size: 3rem;">🍽️</div>
            <p>Gambar {dish_name} siap dalam imajinasi!</p>
        </div>
        """)
        st.markdown(fallback_html, unsafe_allow_html=True)

    st.write("Jangan lupa foto hasil karyamu sebelum disantap! 🍽️")
    st.balloons()
    
    st.divider()

    # Tombol Reset
    if st.button("🏠 Kembali ke Menu Utama", type="primary", use_container_width=True):
        st.session_state.recipe = None
        st.session_state.messages = []
        st.session_state.step_index = 0
        st.session_state.nutrition = None
        st.session_state.shopping = None
        st.rerun()

def render_cooking_view():
    recipe = st.session_state.recipe
    idx = st.session_state.step_index
    total = len(recipe['steps'])
    
    # --- CEK SELESAI ---
    if idx >= total:
        show_finish_dialog(recipe.get('final_image'), recipe['dish'])
        return 

    step_data = recipe['steps'][idx]
    instruction = step_data.get('instruction', str(step_data))
    duration_minutes = step_data.get('duration_minutes', 2)

    # JUDUL
    st.markdown(f"<h2 style='text-align:center; color:#D35400; margin-bottom: 25px;'>🍽️ {recipe['dish']}</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2], gap="large")

    # KOLOM KIRI (INFO)
    with col1:
        render_ingredient_card(recipe['ingredients'])
        render_nutrition_card(st.session_state.nutrition)
        st.write("")
        render_shopping_card(st.session_state.shopping)

    # KOLOM KANAN (LANGKAH & TIMER)
    with col2:
        st.markdown(f"""
            <div style="margin-bottom: 5px; font-weight:600; color:#D35400; font-size:0.9rem;">
                Progress Memasak: {int(((idx) / total) * 100)}%
            </div>
        """, unsafe_allow_html=True)
        st.progress(int(((idx) / total) * 100))
        
        # Render Kartu Langkah
        render_step_card(idx, total, instruction, duration_minutes)
        
        st.write("")
        
        # UPLOAD & VISION
        with st.expander("📸 UPLOAD BUKTI MASAK (Opsional)", expanded=True):
            st.write("Kirim foto untuk dinilai Juri AI:")
            uploaded_file = st.file_uploader("", type=["jpg","png"], key=f"up_{idx}", label_visibility="collapsed")
            
            if uploaded_file:
                image = Image.open(uploaded_file)
                # --- PERBAIKAN DI SINI: Hapus parameter style ---
                st.image(image, width=250) 
            
            st.write("")
            
            btn_col1, btn_col2 = st.columns(2, gap="medium")
            
            with btn_col1:
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
                if st.button("⏩ Lewati Langkah", use_container_width=True):
                    st.info("Langkah dilewati! (Juri tutup mata 🙈)")
                    time.sleep(0.5)
                    st.session_state.step_index += 1
                    st.rerun()

    # CHAT CONSULTANT
    st.divider()
    st.markdown("""
        <p style='color: #2C3E50; font-size: 1rem; font-weight: 600; margin-bottom: 10px; display: flex; align-items: center;'>
            <span style='font-size: 1.4rem; margin-right: 8px;'>💬</span> Tanya Chef Gemoy tentang langkah ini:
        </p>
    """, unsafe_allow_html=True)
    
    with st.container(height=250, border=True):
        for msg in st.session_state.messages:
            render_chat_message(msg["role"], msg["content"])

    user_q = st.chat_input(f"Bingung di langkah {idx+1}?")
    if user_q:
        st.session_state.messages.append({"role": "user", "content": user_q})
        with st.spinner("Chef sedang mengetik..."):
            ans = ask_chef_consultant(user_q, recipe['dish'], instruction)
        st.session_state.messages.append({"role": "assistant", "content": ans})
        st.rerun()

    st.write("")
    if st.button("🔄 Batal Masak / Reset Resep", use_container_width=True, type="secondary"):
        st.session_state.recipe = None
        st.session_state.messages = []
        st.rerun()