# main.py
import streamlit as st
import os

import random
from style import apply_style
from presentation import presentation_et_objectif
from methodologie import methodologie
from dataviz import dataviz
from feature_engineering import feature_engineering
from modelisation import modelisation
from perspectives import perspectives
from perception import perception
from prediction import prediction_page


# Appliquer le style
apply_style()

# Chemin du GIF de navigation
navigation_gif_path = "images/chun-li-walking-animation.gif"

# Titre de la barre latérale
st.sidebar.title("Navigation")

# Vérifier si le GIF de navigation existe
if os.path.exists(navigation_gif_path):
    st.sidebar.image(navigation_gif_path, width=200)
else:
    st.sidebar.write("Erreur : le GIF de navigation est introuvable.")

# Configuration de la barre latérale pour la navigation
page = st.sidebar.selectbox(
    "Choisissez une page",
    [
        "Présentation et Objectif du projet",
        "Méthodologie",
        "DataViz",
        "Feature Engineering",
        "Modélisation",
        "Prédiction",
        "Perception de mon produit",
        "Perspectives",
        "Jeu Surprise",
    ],
)

# Choisir la page à afficher
if page == "Présentation et Objectif du projet":
    presentation_et_objectif()
elif page == "Méthodologie":
    methodologie()
elif page == "DataViz":
    st.title("DataViz")
    dataviz()

elif page == "Feature Engineering":
    feature_engineering()
elif page == "Modélisation":
    st.title("Modélisation")
    modelisation()
elif page == "Prédiction":
    prediction_page()
elif page == "Perspectives":
    perspectives()
elif page == "Perception de mon produit":
    perception()
    # else:
    #  st.error("Le fichier CSV doit contenir une colonne 'user_review'.")
elif page == "Jeu Surprise":
    st.title("THE GAME!!")
    st.write("Es-tu prêt à donner le meilleur de toi même?")
    if st.button("Clique ICI"):
        # Utiliser random.choices avec des poids égaux
        game_choice = random.choices(
            ["casse_brique.py", "snake.py"], weights=[1, 1], k=1
        )[0]
        os.system(f"python {game_choice}")
    # st.write(f"Le jeu {game_choice.split('.')[0]} se lance dans une nouvelle fenêtre.")
