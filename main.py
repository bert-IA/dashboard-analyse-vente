import streamlit as st
import os
from menu import show_menu
from stats import show_stats
from predictions import show_predictions

# Utiliser le port fourni par Heroku
port = int(os.environ.get("PORT", 8501))

# CSS pour plus de visibilité sur le dashboard
st.markdown("""
    <style>
     .stButton button {
            color: black;
            font-weight: bold;
            font-size: 50px;
            padding: 10px 15px; 
            margin: 10px 0; 
            border: 2px solid black; 
            border-radius: 12px;
            cursor: pointer; 
            width: 50%;
            background-color: #f0f0f0;
    }
    .stButton button:hover {
        background-color: black;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialiser l'état de la session
if 'page' not in st.session_state:
    st.session_state.page = 'menu'

# Ajouter des boutons pour naviguer entre les pages
st.sidebar.title("Menu")
if st.sidebar.button('Accueil'):
    st.session_state.page = 'menu'
if st.sidebar.button('Statistiques'):
    st.session_state.page = 'stats'
if st.sidebar.button('Prédictions'):
    st.session_state.page = 'predictions'

# Afficher la page appropriée
if st.session_state.page == 'menu':
    show_menu()
elif st.session_state.page == 'stats':
    show_stats()
elif st.session_state.page == 'predictions':
    show_predictions()

# Lancer l'application Streamlit
if __name__ == "__main__":
    st.run(port=port)