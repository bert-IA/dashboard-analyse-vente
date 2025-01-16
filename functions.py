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
    
    fig, ax = plt.subplots(figsize=(12, 4))
    sns.barplot(data=weekly_sales, x='week', y='sales', ax=ax)
    ax.set_title(f"Ventes par semaine du {start_date.strftime('%Y-%m-%d')} au {end_date.strftime('%Y-%m-%d')}", fontsize=20)
    ax.set_xlabel('Semaine', fontsize=14)
    ax.set_ylabel('Ventes', fontsize=14)
    
    # Ajuster les marges du graphique
    plt.subplots_adjust(top=2, bottom=0.5)
    
    # Ajouter les valeurs au-dessus des barres avec une rotation de 90°, un espacement augmenté et une taille de police réduite
    for p in ax.patches:
        ax.annotate(format(p.get_height(), '.0f'), 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha = 'center', va = 'center', 
                    xytext = (0, 16),  # Augmenter l'espacement ici
                    textcoords = 'offset points', 
                    rotation=90, fontsize=12)  # Réduire la taille de la police
    
    # Conditionnellement supprimer les étiquettes des axes x si le nombre de valeurs dépasse 35
    if len(weekly_sales) > 56:
        ax.set_xticklabels([])
    else:
        ax.set_xticklabels(weekly_sales['week'].dt.strftime('%m-%d'), rotation=90, ha='center')
    
    return fig
