import joblib
import pandas as pd
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


# Télécharger les ressources nécessaires de nltk
nltk.download("stopwords", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("wordnet", quiet=True)

# Charger le modèle et le vectoriseur
log_reg = joblib.load("ML/logistic_regression_model.pkl")
tfidf_vectorizer = joblib.load("ML/tfidf_vectorizer.pkl")

# Initialiser le lemmatizer
lemmatizer = WordNetLemmatizer()


# Fonction de nettoyage du texte
def clean_text(text):
    # Conversion en minuscules
    text = text.lower()

    # Suppression de la ponctuation
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Suppression des chiffres
    text = "".join([i for i in text if not i.isdigit()])

    # Tokenisation
    tokens = word_tokenize(text)

    # Suppression des stop words
    stop_words = set(stopwords.words("english"))
    tokens = [word for word in tokens if word not in stop_words]

    # Lemmatisation
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    # Rejoindre les tokens nettoyés en une chaîne de caractères
    cleaned_text = " ".join(tokens)

    return cleaned_text


# Fonction de prédiction
def predict_user_reviews(uploaded_file):
    if uploaded_file is not None:
        # Lecture du fichier CSV
        try:
            data = pd.read_csv(uploaded_file)
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier : {e}")
            return None, None, None

        # Vérifier que la colonne 'user_review' existe
        if "user_review" not in data.columns:
            print("Erreur : La colonne 'user_review' est manquante.")
            return None, None, None

        # Nettoyer les critiques utilisateur
        data["cleaned_user_review"] = data["user_review"].apply(clean_text)

        # Vectoriser les critiques utilisateur nettoyées
        X = tfidf_vectorizer.transform(data["cleaned_user_review"])

        # Faire des prédictions
        predictions = log_reg.predict(X)

        # Ajouter les prédictions au DataFrame
        data["predictions"] = predictions

        # Calculer les pourcentages de prédictions positives et négatives
        positive_percentage = (predictions == 1).mean() * 100
        negative_percentage = (predictions == 0).mean() * 100

        return data, positive_percentage, negative_percentage
    else:
        print("Aucun fichier uploadé.")
        return None, None, None