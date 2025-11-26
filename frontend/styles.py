import streamlit as st

def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');

    /* --- 1. RESET GLOBAL --- */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    /* Paksa semua teks jadi Abu Gelap agar terbaca */
    p, h1, h2, h3, h4, h5, li, span, label, div {
        color: #2C3E50 !important;
    }
    /* Background Utama Cream Bersih */
    .stApp {
        background-color: #FFFBF2 !important;
    }

    /* --- 2. HEADER MODERN --- */
    .hero-container {
        background: #FFFFFF;
        padding: 2rem;
        border-radius: 24px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(211, 84, 0, 0.08);
        margin-bottom: 2rem;
        border-bottom: 4px solid #D35400;
    }
    .hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #D35400 !important;
        margin: 0;
    }

    /* --- 3. PERBAIKAN INPUT BAR (MENGHILANGKAN KOTAK HITAM) --- */
    /* Ini akan membuat footer menyatu dengan background */
    [data-testid="stBottom"] {
        background-color: #FFFBF2 !important;
        border-top: 1px solid #E0E0E0;
        padding-bottom: 20px;
        padding-top: 20px;
    }
    
    /* Kotak Inputnya Sendiri */
    .stChatInput textarea {
        background-color: #FFFFFF !important;
        color: #333333 !important;
        border: 2px solid #D35400 !important;
        border-radius: 30px !important;
        padding: 12px 20px !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    .stChatInput button {
        color: #D35400 !important;
    }

    /* --- 4. CHAT BUBBLES --- */
    /* Bot */
    div[data-testid="stChatMessage"] {
        background-color: #FFFFFF !important;
        border: 1px solid #EAEAEA;
        border-radius: 20px;
        padding: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
    }
    /* User */
    div[data-testid="stChatMessage"][class*="user"] {
        background-color: #FFE0B2 !important;
        border: none;
    }

    /* --- 5. KARTU RESEP & LANGKAH --- */
    .info-card {
        background: #FFFFFF;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #F0F0F0;
        margin-bottom: 15px;
    }
    .card-header {
        font-weight: 700;
        color: #D35400 !important;
        margin-bottom: 10px;
        font-size: 1.1rem;
    }

    /* --- 6. TOMBOL & UPLOAD --- */
    .stButton button {
        background: #D35400 !important;
        color: white !important;
        border-radius: 50px !important;
        border: none !important;
        padding: 0.5rem 2rem !important;
    }
    .stButton button:hover {
        background: #E65100 !important;
        transform: scale(1.02);
    }

    /* Fix Upload Box agar Putih */
    .streamlit-expanderHeader {
        background-color: #FFFFFF !important;
        color: #D35400 !important;
        border: 1px solid #D35400 !important;
        border-radius: 10px !important;
    }
    [data-testid="stFileUploader"] {
        background-color: #FFF8E1 !important;
        border: 2px dashed #D35400;
        border-radius: 15px;
    }
    [data-testid="stFileUploader"] section { background: transparent !important; }
    
    /* Hide default elements */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)