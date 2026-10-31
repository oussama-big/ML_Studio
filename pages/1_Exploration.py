import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Exploration", layout="wide")
st.title("Exploration des Données")

# --- CHARGEMENT DES DONNÉES (Simplifié pour l'exemple) ---
if 'data' not in st.session_state:
    fichier = st.file_uploader("Chargez un fichier CSV pour commencer :", type=['csv'])
    if fichier:
        st.session_state['data'] = pd.read_csv(fichier)
    else:
        st.info("Veuillez charger un fichier CSV depuis la page d'accueil ou ci-dessus.")
        st.stop()

df = st.session_state['data']

# --- MISE EN PAGE EN 3 SECTIONS ---
col1, col2, col3 = st.columns([1, 1, 2]) # Ratio de largeur des colonnes

# SECTION 1 : Statistiques Globales du Dataset
with col1:
    with st.container(border=True):
        st.subheader("1. Informations Globales")
        st.write(f"**Lignes (Instances) :** {df.shape[0]}")
        st.write(f"**Colonnes (Features) :** {df.shape[1]}")
        
        types = df.dtypes.value_counts()
        st.write("**Types de variables :**")
        for dtype, count in types.items():
            st.write(f"- {dtype} : {count}")
        
        st.write(f"**Valeurs vides totales :** {df.isnull().sum().sum()} ({(df.isnull().sum().sum() / df.size * 100):.2f}%)")

# SECTION 2 : Liste des Features et Sélection
with col2:
        with st.container(border=True , ):

            st.subheader("2. Sélection des Features")
            # Multiselect permet de choisir une ou plusieurs features
            features_selectionnees = st.multiselect(
                "Choisissez les variables à visualiser :",
                options=df.columns.tolist(),
                default=[df.columns[0]] # Sélectionne la première par défaut
            )
            
            if len(features_selectionnees) == 1:
                feature = features_selectionnees[0]
                st.write(f"**Analyse de '{feature}'**")
                st.write(f"- Vides : {df[feature].isnull().sum()} ({(df[feature].isnull().sum() / len(df) * 100):.2f}%)")
                st.write(f"- Uniques : {df[feature].nunique()} ({(df[feature].nunique() / len(df) * 100):.2f}%)")
                if pd.api.types.is_numeric_dtype(df[feature]):
                    st.write(f"- Moyenne : {df[feature].mean():.2f}")
                    st.write(f"- Écart-type : {df[feature].std():.2f}")

# SECTION 3 : Visualisation Dynamique
with col3:
    with st.container(border=True):
        st.subheader("3. Visualisation")
        
        if not features_selectionnees:
            st.info("Sélectionnez au moins une variable dans la colonne 2.")
        
        elif len(features_selectionnees) == 1:
            feature = features_selectionnees[0]
            if pd.api.types.is_numeric_dtype(df[feature]):
                # Histogramme pour les valeurs numériques
                fig = px.histogram(df, x=feature, title=f"Distribution de {feature}")
                st.plotly_chart(fig, use_container_width=True)
            else:
                # Diagramme à barres pour les catégories
                fig = px.bar(df[feature].value_counts().reset_index(), x=feature, y='count', title=f"Fréquence de {feature}")
                st.plotly_chart(fig, use_container_width=True)
                
        elif len(features_selectionnees) == 2:
            f1, f2 = features_selectionnees
            # Nuage de points si les deux sont numériques
            if pd.api.types.is_numeric_dtype(df[f1]) and pd.api.types.is_numeric_dtype(df[f2]):
                fig = px.scatter(df, x=f1, y=f2, title=f"{f2} en fonction de {f1}")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("La visualisation de deux variables nécessite des données numériques pour l'instant.")
        
        else:
            st.warning("Sélectionnez 1 ou 2 variables pour la visualisation détaillée.")

# BOUTON "VISUALIZE ALL" (Pop-out style)
st.markdown("---")
if st.button("👁️ Visualize All (Aperçu global)"):
    st.subheader("Distributions de toutes les variables")
    # Affiche un petit graphique pour chaque variable
    num_cols = df.select_dtypes(include='number').columns
    cols_display = st.columns(3) # Affiche sur 3 colonnes
    for i, col in enumerate(num_cols):
        with cols_display[i % 3]:
            fig = px.histogram(df, x=col, height=200) # Petit graphique
            fig.update_layout(margin=dict(l=20, r=20, t=30, b=20), title=col)
            st.plotly_chart(fig, use_container_width=True)