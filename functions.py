import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def plot_evolution(df, start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    df_filtered = df.loc[(df.index >= start_date) & (df.index <= end_date)]
    
    if df_filtered.empty:
        st.warning("Aucune donnée disponible pour la période donnée.")
        return None
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df_filtered.index, df_filtered['sales'], label='Ventes')
    ax.set_title(f"Ventes du {start_date.strftime('%Y-%m-%d')} au {end_date.strftime('%Y-%m-%d')}", fontsize=20)
    ax.set_xlabel('Date', fontsize=14)
    ax.set_ylabel('Ventes', fontsize=14)
    ax.legend()
    
    return fig

def plot_ventes_par_semaine(df, start_date, end_date):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    df_filtered = df.loc[(df.index >= start_date) & (df.index <= end_date)].copy()
    df_filtered['week'] = df_filtered.index.to_period('W').start_time
    
    weekly_sales = df_filtered.groupby('week')['sales'].sum().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=weekly_sales, x='week', y='sales', ax=ax)
    ax.set_title(f"Ventes par semaine du {start_date.strftime('%Y-%m-%d')} au {end_date.strftime('%Y-%m-%d')}", fontsize=20)
    ax.set_xlabel('Semaine', fontsize=14)
    ax.set_ylabel('Ventes', fontsize=14)
    # Formater les dates pour afficher uniquement le mois et le jour
    ax.set_xticklabels(weekly_sales['week'].dt.strftime('%m-%d'), rotation=45, ha='right')
    
    return fig
