import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from functions import plot_evolution, plot_ventes_par_semaine

def show_stats():
    st.title("Statistiques des ventes")
    
    # Charger les données
    df = pd.read_csv('data/data_stat.csv')
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    def plot_ventes_par_jour_semaine(df, start_date, end_date):
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        
        df_filtered = df.loc[(df.index >= start_date) & (df.index <= end_date)].copy()
        df_filtered['day_of_week'] = df_filtered.index.day_name()
        
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dfs = {day: df_filtered.loc[df_filtered['day_of_week'] == day] for day in days_of_week}
        
        figures = {}
        for day in days_of_week:
            if day in dfs:
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.barplot(data=dfs[day], x=dfs[day].index, y='sales', ax=ax)
                ax.set_title(f"{day} : ventes du {start_date.strftime('%Y-%m-%d')} au {end_date.strftime('%Y-%m-%d')}", fontsize=20)
                ax.set_xlabel('Date', fontsize=14)
                ax.set_ylabel('Ventes', fontsize=14)
                # Formater les dates pour afficher uniquement le mois et le jour
                ax.set_xticklabels(dfs[day].index.strftime('%m-%d'), rotation=45, ha='right')
                # Ajouter une ligne horizontale pour la moyenne des ventes
                mean_sales = dfs[day]['sales'].mean()
                ax.axhline(mean_sales, color='red', linestyle='--', label=f'Moyenne des ventes ({mean_sales:.2f})')
                ax.legend(fontsize=14)
                figures[day] = fig
        
        return figures

    def analyse_ventes(df, start_date, end_date):
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        
        df_filtered = df.loc[(df.index >= start_date) & (df.index <= end_date)]
        if df_filtered.empty:
            return pd.DataFrame(columns=['date', 'day_of_week', 'sales']), None
        
        Q1 = df_filtered['sales'].quantile(0.25)
        Q3 = df_filtered['sales'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outliers = df_filtered.loc[(df_filtered['sales'] < lower_bound) | (df_filtered['sales'] > upper_bound)].copy().reset_index()
        outliers['date'] = outliers['date'].dt.date  # Convert to date to remove hours, minutes, and seconds
        outliers['day_of_week'] = outliers['date'].apply(lambda x: x.strftime('%A'))  # Get the day name
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(y='sales', data=df_filtered, ax=ax)
        ax.set_title(f"Période du {start_date.strftime('%Y-%m-%d')} au {end_date.strftime('%Y-%m-%d')}", fontsize=20)
        ax.set_ylabel('Ventes', fontsize=14)
        
        ax.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
        ax.grid(True, which='major', axis='y', linestyle='--', linewidth=0.5)
        
        return outliers[['date', 'day_of_week', 'sales']], fig

    # Sélecteurs de dates
    st.markdown("<h3 style='font-size:30px; font-weight:bold;'>Date de début</h3>", unsafe_allow_html=True)
    start_date = st.date_input("", df.index.min(), key='start_date')
    st.markdown("<h3 style='font-size:30px; font-weight:bold;'>Date de fin</h3>", unsafe_allow_html=True)
    end_date = st.date_input("", df.index.max(), key='end_date')

    # Bouton pour afficher l'évolution des ventes
    if st.button("Afficher l'évolution des ventes"):
        st.session_state.show_sales_evolution = True

    if st.session_state.get('show_sales_evolution', False):
        st.subheader("Evolutions des ventes ")
        fig_ventes_evolution = plot_evolution(df, start_date, end_date)
        if fig_ventes_evolution:
            st.pyplot(fig_ventes_evolution)
        
        # Bouton pour afficher l'analyse statistique
        if st.button("Analyse statistique"):
            st.session_state.show_stat_analyse = True

        if st.session_state.get('show_stat_analyse', False):
            st.subheader("Répartition des ventes ")
            outliers_df, fig_boxplot = analyse_ventes(df, start_date, end_date)
            if fig_boxplot:
                st.pyplot(fig_boxplot)
            
            st.subheader("Ventes exceptionnelles")
            st.write(outliers_df)
        
        # Bouton pour afficher l'analyse des ventes par jour de la semaine
        if st.button("Analyse des ventes suivant le jour de la semaine"):
            st.session_state.show_day_analysis = True

        if st.session_state.get('show_day_analysis', False):
            st.subheader("Ventes par jour de la semaine")
            day_of_week = st.radio("Choisissez un jour de la semaine", ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
            figures = plot_ventes_par_jour_semaine(df, start_date, end_date)
            if day_of_week in figures:
                st.pyplot(figures[day_of_week])
        
        # Bouton pour afficher l'analyse des ventes par semaine
        if st.button("Analyse par semaine"):
            st.session_state.show_week_analysis = True

        if st.session_state.get('show_week_analysis', False):
            st.subheader("Ventes par semaine")
            fig_sales_by_week = plot_ventes_par_semaine(df, start_date, end_date)
            if fig_sales_by_week:
                st.pyplot(fig_sales_by_week)
