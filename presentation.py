# presentation.py
import streamlit as st
from PIL import Image
import os
import pandas as pd


def presentation_et_objectif():
    image_path1 = "images/image_pres.png"
    image_path2 = "images/street.png"

    if os.path.exists(image_path1):
        st.image(image_path1, use_column_width=True)
    else:
        st.write("Erreur : l'image de présentation est introuvable.")

    st.title("Présentation du projet")

    st.markdown(
        """
        Dans le cadre de notre formation en analyse de données et en vue de développer nos compétences pratiques, nous avons choisi d'explorer et d'analyser les ventes de jeux vidéo.
    """
    )

    st.header("Définition des Objectifs Principaux")
    st.markdown(
        """
        Pour ce projet, il faudra estimer les ventes totales d'un jeu vidéo à l'aide d'informations descriptives. Il va alors falloir passer par plusieurs étapes dont :

        - **Exploration des Données** : Comprendre la structure des données et identifier les principales caractéristiques qui influencent les ventes de jeux vidéo.
        - **Visualisation des Données** : Créer des visualisations interactives pour mettre en évidence les tendances et les relations dans les données.
        - **Pré-processing des Données** : Nettoyer et préparer les données pour une analyse plus approfondie pour des modèles prédictifs.
        - **Modélisation** : Entraînements de modèles de machine learning sur des données afin de prédire les ventes globales des jeux vidéo.
        - **Analyse et Interprétation** : Comprendre les résultats obtenus et en tirer des conclusions pertinentes.
        - **Features Engineering** : Améliorer les résultats du modèle en créant de nouvelles variables à partir des données existantes.
    """
    )

    if os.path.exists(image_path2):
        st.image(image_path2, use_column_width=True)
    else:
        st.write("Erreur : l'image de données est introuvable.")

    st.markdown(
        """
    Voici une description détaillée des jeux de données utilisés :

    ### VGChartz

    ### Statistiques des Jeux Vidéos

    Initialement, nous avons utilisé les données disponibles sur VGChartz. Cependant, nous avons constaté que certaines informations cruciales manquaient. Pour pallier ce manque, nous avons :

    - **Rescrappé VGChartz** : Pour obtenir une version plus complète et actualisée des données de vente.
    - **Scrappé Metacritic** : Pour intégrer des données supplémentaires sur les scores des utilisateurs et de la presse.

    ### Metacritic

    ### Volumétrie du Jeu de Données Final
    Après avoir combiné les données scrappées de VGChartz, Metacritic et le jeu de données supplémentaires, notre DataFrame final nettoyé contient plus de 14 500 entrées (sans outliers) et 16 325 (avec outliers).
    """
    )

    df = pd.read_csv("Data/Ventes_jeux_video_final.csv")

    st.write("Dataset après scrapping")
    st.write(df)
