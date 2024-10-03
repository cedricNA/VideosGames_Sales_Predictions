import streamlit as st
import pandas as pd
import lightgbm as lgb
import joblib
import warnings

# Charger les données et le modèle
df_top = pd.read_csv("Data/df_topfeats.csv")
df_features = pd.read_csv("Data/df_features.csv")
model = lgb.Booster(model_file="ML/model_final.txt")
warnings.simplefilter(action="ignore", category=pd.errors.PerformanceWarning)


def get_input():
    st.sidebar.header("Sélection des entrées")

    input_data = {}
    publisher_input = st.sidebar.selectbox(
        "Sélectionnez l'éditeur", df_features["Publisher"].unique()
    )
    genre_input = st.sidebar.selectbox(
        "Sélectionnez le genre", df_features["Genre"].unique()
    )
    platform_input = st.sidebar.selectbox(
        "Sélectionnez la plateforme", df_features["Platform"].unique()
    )
    years = list(range(1980, 2031))
    year_input = st.sidebar.selectbox(
        "Sélectionnez l'année", years, index=years.index(2024)
    )
    input_data["Year"] = year_input

    meta_input = st.sidebar.number_input(
        "Sélectionnez le score Metacritic",
        min_value=0.0,
        max_value=100.0,
        value=float(df_features["meta_score"].mean()),
        format="%.0f",
    )
    input_data["meta_score"] = meta_input

    user_input = st.sidebar.number_input(
        "Sélectionnez le score utilisateur",
        min_value=0.0,
        max_value=100.0,
        value=float(df_features["user_review"].mean()),
        format="%.1f",
    )
    input_data["user_review"] = user_input

    return publisher_input, genre_input, platform_input, input_data


def get_features(input_data, df_features, genre_input, platform_input):
    input_data["Global_Sales_mean_genre"] = df_features[
        df_features["Genre"] == genre_input
    ]["Global_Sales_mean_genre"].mean()
    input_data["Global_Sales_mean_platform"] = df_features.loc[
        df_features["Platform"] == platform_input
    ]["Global_Sales_mean_platform"].mean()
    input_data["Year_Global_Sales_mean_genre"] = (
        input_data["Year"] * input_data["Global_Sales_mean_genre"]
    )
    input_data["Year_Global_Sales_mean_platform"] = (
        input_data["Year"] * input_data["Global_Sales_mean_platform"]
    )

    df_input_data = pd.DataFrame(input_data, index=[0])

    cumulative_sales_genre = (
        df_features[
            (df_features["Genre"] == genre_input)
            & (df_features["Year"] <= input_data["Year"])
        ]
        .sort_values("Year")["Global_Sales"]
        .cumsum()
        .iloc[-1]
    )

    df_input_data["Cumulative_Sales_Genre"] = cumulative_sales_genre

    cumulative_sales_platform = (
        df_features[
            (df_features["Platform"] == platform_input)
            & (df_features["Year"] <= input_data["Year"])
        ]
        .sort_values("Year")["Global_Sales"]
        .cumsum()
        .iloc[-1]
    )

    df_input_data["Cumulative_Sales_Platform"] = cumulative_sales_platform

    return df_input_data


def standardization(df_input_data, publisher_input):
    numerical_features = [
        "Year",
        "meta_score",
        "user_review",
        "Global_Sales_mean_genre",
        "Global_Sales_mean_platform",
        "Year_Global_Sales_mean_genre",
        "Year_Global_Sales_mean_platform",
        "Cumulative_Sales_Genre",
        "Cumulative_Sales_Platform",
    ]

    numerical_transformer = joblib.load("ML/numerical_transformer.joblib")
    df_input_data[numerical_features] = numerical_transformer.transform(
        df_input_data[numerical_features]
    )

    publisher_cols = ["Publisher_" + str(pub) for pub in df_top["Publisher"].unique()]
    for col in publisher_cols:
        df_input_data[col] = 0
    df_input_data["Publisher_" + publisher_input] = 1

    df_input_data = df_input_data.drop(["Publisher_10TACLE Studios"], axis=1)

    return numerical_features, df_input_data


def prediction_page():
    st.title("Prédiction des ventes de jeux vidéo")

    # CSS pour positionner l'écran de la borne d'arcade
    st.markdown(
        """
        <style>
        .arcade-container {
            position: relative;
            text-align: center;
            color: white;
            max-width: 800px;
            margin: 0 auto;
        }
        .arcade-image {
            width: 100%;
            height: auto;
        }
        .arcade-screen {
            font-family: 'Press Start 2P', cursive;
            color: #ec8853;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
            font-size : 22px;
            position: absolute;
            top: -450px; /* Ajustez cette valeur pour positionner le texte correctement */
            left: 72%;
            transform: translate(-50%, -50%);
            width: 65%; /* Ajustez cette valeur selon vos besoins */
            height: 200px; /* Ajustez cette valeur selon vos besoins */
            display: flex;
            align-items: center;
            justify-content: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Afficher l'image de la borne d'arcade
    st.image("images/street_arcade.jpg", width=1000)

    # Obtenir les entrées utilisateur
    publisher_input, genre_input, platform_input, input_data = get_input()

    if st.sidebar.button("Prédire"):
        # Obtenir les caractéristiques
        df_input_data = get_features(
            input_data, df_features, genre_input, platform_input
        )

        # Standardiser les données
        numerical_features, df_input_data_transformed = standardization(
            df_input_data, publisher_input
        )

        # Prédire en fonction des entrées utilisateur
        user_pred = model.predict(df_input_data_transformed)

        # Superposer la prédiction sur l'image de la borne d'arcade
        st.markdown(
            f"""
        <div class="arcade-container">
            <div class="arcade-screen">Prédiction pour les ventes:<br><br> {user_pred[0]:.4f} millions d'unités</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
        <div class="arcade-container">
            <div class="arcade-screen">Entrez les informations nécessaires pour prédire les ventes globales d'un jeu vidéo</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    # st.header("Entrez les informations nécessaires pour prédire les ventes globales d'un jeu vidéo.")


# Exécuter l'application
if __name__ == "__main__":
    prediction_page()
