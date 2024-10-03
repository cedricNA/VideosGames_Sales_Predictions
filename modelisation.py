import streamlit as st
import lightgbm as lgb
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.datasets import fetch_california_housing
from sklearn.metrics import mean_squared_error


def modelisation():

    # Titre de la présentation
    st.title("🚀 Présentation du Modèle LightGBM")

    # Introduction
    st.header("Introduction 🌟")
    st.write(
        """
    Avant de sélectionner le modèle ci-dessous, nous avons utilisé un LazyRegressor qui a généré 29 modèles et leurs scores respectifs. Le LightGBM ayant obtenu les meilleurs résultats, c'est celui que nous avons choisi pour ce projet.                   
    LightGBM est un framework de boosting de gradient développé par Microsoft. Il est conçu pour être extrêmement efficace, rapide et performant.
    """
    )

    # Fonctionnement de LightGBM
    st.header("Fonctionnement de LightGBM 🛠️")

    st.write(
        """
    Le LightGBM Regressor fonctionne en combinant plusieurs techniques avancées pour optimiser l'entraînement et la précision des modèles de régression :
    Gradient Boosting : Combine plusieurs modèles faibles séquentiellement pour créer un modèle puissant.
             
    Exclusive Feature Bundling (EFB) : Réduit la dimensionnalité en combinant des variables non chevauchantes.
             
    Gradient-based One-Side Sampling (GOSS) : Améliore l'efficacité de l'entraînement en sélectionnant intelligemment les échantillons de données.
    Croissance verticale des arbres : Ajoute des niveaux de profondeur aux arbres de décision pour améliorer les prédictions.
    """
    )

    # Schéma de fonctionnement de LightGBM
    chemin_image = os.path.join(
        os.getcwd(), "images", "A_stylized_diagram_illustrating_the_workflow_of_Li.jpg"
    )
    st.subheader("Schéma de Fonctionnement 🔍")
    st.image(
        chemin_image,
        caption="Schéma de Fonctionnement de LightGBM",
        use_column_width=True,
    )

    # Avantages de LightGBM
    st.header("Avantages de LightGBM 💡")

    st.write(
        """
    - **Vitesse et Efficacité** : LightGBM est conçu pour être très rapide et efficace.
    - **Précision** : Grâce à ses techniques avancées de boosting, il offre une grande précision.
    - **Scalabilité** : Il peut gérer des ensembles de données volumineux avec de nombreuses fonctionnalités.
    - **Support des Valeurs Manquantes** : LightGBM gère nativement les valeurs manquantes.
    """
    )

    # Schéma des avantages
    st.subheader("Avantages en un coup d'œil 📊")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(
        ["Vitesse", "Précision", "Scalabilité", "Support des Valeurs Manquantes"],
        [90, 85, 95, 80],
        color="skyblue",
    )
    ax.set_xlabel("Importance (%)")
    ax.set_title("Avantages de LightGBM")
    st.pyplot(fig)
    plt.close(fig)  # Ferme la figure après l'affichage

    # Interactivité avec l'utilisateur
    st.header("Essayez par vous-même ! 🎮")

    # Slider interactif pour ajuster les paramètres (exemple)
    max_depth = st.slider("Choisissez la profondeur maximale de l'arbre", 1, 20, 6)
    learning_rate = st.slider("Choisissez le taux d'apprentissage", 0.01, 0.5, 0.1)

    # Chargement des données
    data = fetch_california_housing()
    X = pd.DataFrame(data.data, columns=data.feature_names)
    y = pd.Series(data.target, name="target")

    # Division des données
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Création et entraînement du modèle avec les paramètres ajustés
    model = lgb.LGBMRegressor(max_depth=max_depth, learning_rate=learning_rate)
    model.fit(X_train, y_train)

    # Prédiction et évaluation
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)

    # Affichage des résultats
    st.write(
        f"Erreur Quadratique Moyenne (MSE) avec profondeur {max_depth} et taux d'apprentissage {learning_rate}: {mse:.2f}"
    )

    # Comparaison des valeurs prédites et réelles
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(y_test, y_pred, alpha=0.3)
    ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], "r--", lw=2)
    ax.set_xlabel("Valeurs réelles")
    ax.set_ylabel("Valeurs prédites")
    ax.set_title("Comparaison des valeurs réelles et prédites")
    st.pyplot(fig)
    plt.close(fig)  # Ferme la figure après l'affichage

    # Conclusion
    st.header("Conclusion 🎯")
    st.write(
        """
            LightGBM est un outil puissant pour les tâches de régression et de classification, particulièrement adapté aux grands ensembles de données.

            Score du modèle avant feature engineering :

            LGBMRegressor R² : Moyenne = 0.3107, Écart-type = 0.0151
            LGBMRegressor MSE : Moyenne = 0.0400, Écart-type = 0.0027
            LGBMRegressor MAE : Moyenne = 0.1432, Écart-type = 0.0043
            
            Score du modèle après feature engineering :

            LGBMRegressor R² : Moyenne = 0.9880, Écart-type = 0.0035
            LGBMRegressor MSE : Moyenne = 0.0007, Écart-type = 0.0002
            LGBMRegressor MAE : Moyenne = 0.0132, Écart-type = 0.0013
"""
    )

    # Ajout d'un GIF fun lié aux jeux vidéo
    st.markdown(
        """
    <div style="display: flex; justify-content: center;">
        <iframe src="https://giphy.com/embed/mHv5sLKI1b1I8r4wmp" width="680" height="370" frameBorder="0" class="giphy-embed" allowFullScreen></iframe>
    </div>
    """,
        unsafe_allow_html=True,
    )
