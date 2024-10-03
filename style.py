# style.py
import streamlit as st


def apply_style():
    # CSS pour personnaliser la barre latérale et les titres
    st.markdown(
        """
        <head>
            <!-- Import de la police pixélisée -->
            <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Tiny5&display=swap" rel="stylesheet">
            <style>
            /* Style pour la barre latérale */
            [data-testid="stSidebar"] {
                background-color: #FFD580; /* Couleur orange douce */
            }

            h1, h2, h3, h4, h5, h6 {
                font-family: 'Tiny5', sans-serif !important;
                color: #003366; /* Couleur bleu marine */
            }
            </style>
        </head>
        """,
        unsafe_allow_html=True,
    )
