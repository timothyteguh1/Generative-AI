import streamlit as st
from config import configure_ai, setup_folders
from frontend.styles import load_css
from frontend.components import render_header

# Import Views
from frontend.views.home_view import render_home_view
from frontend.views.cooking_view import render_cooking_view

# --- SETUP ---
st.set_page_config(page_title="ChefBot Pro", page_icon="👨‍🍳", layout="wide", initial_sidebar_state="collapsed")
configure_ai()
setup_folders()
load_css()

# --- STATE ---
if "recipe" not in st.session_state:
    st.session_state.recipe = None
    st.session_state.nutrition = None
    st.session_state.step_index = 0
    st.session_state.shopping = None
    st.session_state.messages = [{"role": "assistant", "content": "Halo! ChefBot siap bantu. Mau masak apa hari ini?"}]

# --- RENDER UI ---
render_header()

if st.session_state.recipe is None:
    # Tampilkan View Home jika belum ada resep
    render_home_view()
else:
    # Tampilkan View Masak jika resep sudah aktif
    render_cooking_view()