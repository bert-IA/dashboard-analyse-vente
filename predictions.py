import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from functions import plot_evolution, plot_ventes_par_semaine

def show_predictions():
    st.title("Prédiction des ventes pour l'année 2017")
    
   
    # Charger les prédictions
    pred_df = pd.read_csv('data/prediction.csv')
    
     
    #vérifier si la date existe
    if 'date' not in pred_df.columns:
        st.error("The 'date' column is missing from the data.")
        return
    
    pred_df['date'] = pd.to_datetime(pred_df['date'])
    pred_df.set_index('date', inplace=True)
    
    # Sélecteurs de dates
    st.markdown("<h3 style='font-size:30px; font-weight:bold;'>Date de début</h3>", unsafe_allow_html=True)
    start_date = st.date_input("", pred_df.index.min(), key='start_date')
    st.markdown("<h3 style='font-size:30px; font-weight:bold;'>Date de fin</h3>", unsafe_allow_html=True)
    end_date = st.date_input("", pred_df.index.max(), key='end_date')

    # Bouton pour afficher les prédictions
    if st.button("Afficher les prédictions"):
        st.session_state.show_predictions = True

    if st.session_state.get('show_predictions', False):
        st.subheader("Prédictions des ventes")
        fig_predictions = plot_evolution(pred_df, start_date, end_date)
        if fig_predictions:
            st.pyplot(fig_predictions)
        
        # Bouton pour afficher les prédictions par semaine
        if st.button("Prédictions par semaine"):
            st.session_state.show_weekly_predictions = True

        if st.session_state.get('show_weekly_predictions', False):
            st.subheader("Prédictions des ventes par semaine")
            fig_weekly_predictions = plot_ventes_par_semaine(pred_df, start_date, end_date)
            if fig_weekly_predictions:
                st.pyplot(fig_weekly_predictions)
