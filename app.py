import streamlit as st
from PIL import Image
import time

# --- IMPORT AGENTS ---
try:
    from agents.planner import generate_recipe_plan
    from agents.vision import evaluate_cooking_step
    from agents.consultant import ask_chef_consultant
    from agents.nutritionist import analyze_nutrition # <--- TAMBAHAN 1: Import Agent Baru
except ImportError:
    st.error("⚠️ Folder 'agents' belum siap.")
    st.stop()

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="ChefBot Kitchen",
    page_icon="👨‍🍳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# CSS PERBAIKAN (THEME FORCER)
# ==========================================
st.markdown("""
    <style>
    /* Import Font */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700&display=swap');

    /* 1. PAKSA TEXT JADI HITAM (Mengatasi Invisible Text) */
    html, body, p, span, div, h1, h2, h3, h4, h5, h6, li, label {
        font-family: 'Outfit', sans-serif;
        color: #2C3E50 !important; /* Warna Abu Gelap Solid */
    }
    
    /* 2. BACKGROUND UTAMA (Cream) */
    .stApp {
        background-color: #FFFBF2 !important;
    }

    /* 3. PERBAIKAN HEADER */
    .hero-container {
        background: #FFFFFF;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        margin-bottom: 2rem;
        border-bottom: 5px solid #D35400;
    }
    .hero-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #D35400 !important;
        margin: 0;
    }
    .hero-subtitle {
        color: #7F8C8D !important;
        margin-top: 10px;
    }

    /* 4. PERBAIKAN CHAT BUBBLE (Agar teks terbaca) */
    .stChatMessage {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E5E5;
        border-radius: 18px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
    }
    .stChatMessage p {
        color: #333333 !important; /* Paksa teks chat jadi hitam */
    }
    /* Chat User */
    div[data-testid="stChatMessage"][class*="user"] {
        background-color: #FFE0B2 !important;
        border: none;
    }

    /* 5. MEMPERCANTIK INPUT BAR (MENGHILANGKAN KOTAK HITAM) */
    
    /* Paksa Container Bawah jadi sewarna background, bukan hitam */
    [data-testid="stBottom"] {
        background-color: #FFFBF2 !important; 
        border-top: 1px solid #E0E0E0;
        padding-bottom: 20px;
    }
    [data-testid="stBottom"] > div {
        background-color: transparent !important;
    }

    /* Styling Kotak Inputnya (Pill Shape) */
    .stChatInput textarea {
        background-color: #FFFFFF !important; /* Latar putih */
        color: #333333 !important; /* Teks ketikan hitam */
        border: 2px solid #D35400 !important; /* Border oranye */
        border-radius: 30px !important; /* Bulat */
        padding: 10px 20px !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    /* Placeholder text (Teks 'Ketik disini...') */
    .stChatInput textarea::placeholder {
        color: #999999 !important;
    }
    
    /* Icon kirim */
    .stChatInput button {
        color: #D35400 !important;
    }

    /* 6. RECIPE CARDS STYLE */
    .recipe-card, .step-card {
        background: #FFFFFF;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        height: 100%;
        color: #333333 !important;
    }
    .recipe-card { border-top: 5px solid #F39C12; }
    .step-card { border-top: 5px solid #D35400; }
    
    ul, ol { color: #333333 !important; }
    
    /* Sembunyikan elemen mengganggu */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* ============================================= */
    /* FIX HEADER EXPANDER (AGAR TIDAK HITAM SAAT DIBUKA) */
    /* ============================================= */

    /* 1. Style Dasar (Saat Tertutup & Terbuka) */
    .streamlit-expanderHeader {
        background-color: #FFFFFF !important;      /* SELALU Putih (Hapus Hitam) */
        color: #D35400 !important;                 /* Teks Oranye */
        border: 2px solid #D35400 !important;      /* Borderline Oranye Tegas */
        border-radius: 10px !important;            /* Sudut membulat */
    }

    /* 2. Menghapus background hitam bawaan saat Focus/Active */
    .streamlit-expanderHeader:focus, 
    .streamlit-expanderHeader:active,
    .streamlit-expanderHeader[aria-expanded="true"] { 
        background-color: #FFFFFF !important;      /* Paksa tetap Putih saat dibuka */
        color: #D35400 !important;
    }

    /* 3. Efek Hover (Saat mouse di atasnya) */
    .streamlit-expanderHeader:hover {
        background-color: #FFF3E0 !important;      /* Cream muda saat hover */
        border-color: #E65100 !important;          /* Border lebih gelap */
        color: #E65100 !important;
    }

    /* 4. Mengubah warna Panah (Arrow Icon) */
    .streamlit-expanderHeader svg {
        color: #D35400 !important;
        fill: #D35400 !important;
    }

    /* TAMBAHAN 2: CSS KHUSUS KARTU NUTRISI (Agar sesuai tema) */
    .nutrition-card {
        background: #F1F8E9; /* Hijau Sangat Muda */
        padding: 20px; 
        border-radius: 20px;
        border: 1px dashed #66BB6A; /* Garis Hijau */
        margin-top: 20px;
        text-align: center;
    }
    .nutri-value { font-size: 1.2rem; font-weight: 700; color: #2E7D32 !important; }
    .nutri-label { font-size: 0.8rem; color: #558B2F !important; text-transform: uppercase; letter-spacing: 1px;}
    </style>
""", unsafe_allow_html=True)

# --- STATE MANAGEMENT ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Halo! Saya ChefBot. Mau masak apa hari ini?"}]
if "recipe" not in st.session_state:
    st.session_state.recipe = None
if "nutrition" not in st.session_state: # <--- TAMBAHAN 3: State Nutrisi
    st.session_state.nutrition = None
if "step_index" not in st.session_state:
    st.session_state.step_index = 0

# ==========================================
# HEADER HERO
# ==========================================
st.markdown("""
    <div class="hero-container">
        <div class="hero-title">👨‍🍳 ChefBot Kitchen</div>
        <div class="hero-subtitle">Asisten Masak Pintar dengan Artificial Intelligence</div>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# LOGIKA APLIKASI
# ==========================================

# MODE 1: BELUM ADA RESEP
if not st.session_state.recipe:
    # Chat History
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # Input
    user_input = st.chat_input("Mau masak apa? (Contoh: Nasi Goreng)")
    
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"): 
            st.markdown(user_input)
        
        # 1. Generate Resep
        with st.spinner("🔥 Chef sedang meracik resep..."):
            recipe_data = generate_recipe_plan(user_input)
            
        if recipe_data:
            # 2. Generate Nutrisi (TAMBAHAN 4: Panggil Agent Nutrisi)
            with st.spinner("🍎 Ahli Gizi sedang menghitung kalori..."):
                nutri_data = analyze_nutrition(recipe_data)

            st.session_state.recipe = recipe_data
            st.session_state.nutrition = nutri_data # Simpan data nutrisi
            st.session_state.step_index = 0
            st.session_state.messages = []
            st.rerun()

# MODE 2: DASHBOARD MASAK
elif st.session_state.recipe:
    recipe = st.session_state.recipe
    nutri = st.session_state.nutrition # Ambil data nutrisi
    current_step_idx = st.session_state.step_index
    total_steps = len(recipe['steps'])
    current_instruction = recipe['steps'][current_step_idx]
    
    st.markdown(f"<h2 style='text-align:center; margin-bottom:20px; color:#D35400 !important;'>🍽️ {recipe['dish']}</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 2], gap="large")

    # KIRI: Bahan & Nutrisi
    with col1:
        # Kartu Bahan
        ing_list = "".join([f"<li style='margin-bottom:8px; color:#444;'>{i}</li>" for i in recipe['ingredients']])
        st.markdown(f"""
        <div class="recipe-card">
            <h3 style="color:#F39C12 !important; margin-top:0;">🛒 Bahan-Bahan</h3>
            <ul style="padding-left:20px;">{ing_list}</ul>
        </div>
        """, unsafe_allow_html=True)

        # TAMBAHAN 5: Kartu Nutrisi (Ditampilkan jika ada data)
        if nutri:
            st.markdown(f"""
            <div class="nutrition-card">
                <h4 style="color:#2E7D32 !important; margin-top:0;">🍎 Info Gizi (Per Porsi)</h4>
                <div style="display:flex; justify-content:space-around; margin-top:15px;">
                    <div>
                        <div class="nutri-value">{nutri.get('calories', '-')}</div>
                        <div class="nutri-label">Kalori</div>
                    </div>
                    <div>
                        <div class="nutri-value">{nutri.get('protein', '-')}</div>
                        <div class="nutri-label">Protein</div>
                    </div>
                </div>
                <div style="display:flex; justify-content:space-around; margin-top:10px;">
                    <div>
                        <div class="nutri-value">{nutri.get('carbs', '-')}</div>
                        <div class="nutri-label">Karbo</div>
                    </div>
                    <div>
                        <div class="nutri-value">{nutri.get('fats', '-')}</div>
                        <div class="nutri-label">Lemak</div>
                    </div>
                </div>
                <hr style="border-top: 1px dashed #A5D6A7; margin: 15px 0;">
                <p style="font-size:0.9rem; font-style:italic; color:#33691E !important; margin:0;">
                    💡 "{nutri.get('health_tip', 'Makanlah dengan bijak!')}"
                </p>
            </div>
            """, unsafe_allow_html=True)

    # KANAN: Langkah
    with col2:
        prog = int(((current_step_idx + 1) / total_steps) * 100)
        st.progress(prog)
        
        st.markdown(f"""
        <div class="step-card">
            <h3 style="color:#D35400 !important; margin-top:0;">🔥 Langkah {current_step_idx + 1} / {total_steps}</h3>
            <p style="font-size:1.3rem; font-weight:500; line-height:1.5; color:#222;">{current_instruction}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("") 

        # Upload Area
        with st.expander("📸 UPLOAD BUKTI MASAK", expanded=True):
            uploaded_file = st.file_uploader("Upload foto:", type=["jpg", "png"], key=f"up_{current_step_idx}")
            
            if uploaded_file:
                image = Image.open(uploaded_file)
                st.image(image, width=250)
                
                if st.button("🔍 Nilai Masakan"):
                    with st.spinner("Menilai..."):
                        res = evaluate_cooking_step(image, current_instruction)
                    
                    if res['status'] == 'PASS':
                        st.success(f"✅ {res['feedback']}")
                        time.sleep(2)
                        st.session_state.step_index += 1
                        if st.session_state.step_index >= total_steps:
                            st.balloons()
                            st.session_state.recipe = None
                            st.session_state.nutrition = None # Reset nutrisi
                            st.session_state.messages = [{"role": "assistant", "content": "Selesai! Selamat makan."}]
                        st.rerun()
                    else:
                        st.error(f"❌ {res['feedback']}")

    # Q&A History
    st.markdown("---")
    st.caption("💬 Riwayat Tanya Jawab:")
    with st.container(height=200):
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # Fixed Input Chat
    user_q = st.chat_input(f"Tanya tentang langkah {current_step_idx + 1}...")
    if user_q:
        st.session_state.messages.append({"role": "user", "content": user_q})
        with st.spinner("Menjawab..."):
            answer = ask_chef_consultant(user_q, recipe['dish'], current_instruction)
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()
        
    if st.button("🔄 Reset"):
        st.session_state.recipe = None
        st.session_state.nutrition = None
        st.session_state.messages = []
        st.rerun()