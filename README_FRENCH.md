# VideosGames_Sales_Predictions

Bienvenue dans le projet **Video Games Sales Predictions**, une application interactive déployée sur **Streamlit** qui permet de prédire les ventes globales de jeux vidéo et d'analyser la perception des utilisateurs en fonction de leurs avis.

[Visitez l'application ici](https://videosgamessalespredictions.streamlit.app/)

## Fonctionnalités

- **Prédiction des ventes** : Utilisez l'interface pour prédire les ventes globales d'un jeu vidéo en sélectionnant des informations telles que l'éditeur, le genre, la plateforme, l'année de sortie, et plus encore.
- **Perception de mon produit** : Téléchargez un fichier CSV contenant des avis utilisateurs et laissez l'algorithme prédire la perception des clients sur votre produit en analysant les avis.
- **Visualisation des résultats** : Les résultats sont affichés de manière claire et concise, sous forme de texte ou de graphiques interactifs.
- **Interface inspirée des jeux rétro** : L'interface rappelle les anciennes bornes d'arcade pour offrir une expérience nostalgique tout en interagissant avec des données modernes.

## Prérequis

Pour exécuter ce projet localement, vous devez avoir **Python 3.x** installé ainsi que toutes les dépendances nécessaires.

### Installation

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/cedricna/videosgames_sales_predictions.git
   cd videosgames_sales_predictions

2. **Créer et activer un environnement virtuel**:

- Sur Linux/macOS :
  ```bash
  python3 -m venv venv
  source venv/bin/activate

- Sur Windows :
   ```bash
   python -m venv venv
   .\venv\Scripts\activate

 3. **Installer les dépendances** :  
  ```bash
   pip install -r requirements.txt
```
 
### Exécution locale

Une fois les dépendances installées, lancez l'application **Streamlit** en local avec la commande suivante :

```bash
streamlit run main.py
```
Cela ouvrira l'application dans votre navigateur par défaut à l'adresse http://localhost:8501.    

## Utilisation
### Prédiction des ventes
L'interface utilisateur vous permet de prédire les ventes d'un jeu vidéo en sélectionnant les informations suivantes :

1. **Éditeur** : Sélectionnez l'éditeur du jeu parmi une liste d'éditeurs populaires.
2. **Genre** : Choisissez le genre du jeu (action, sport, etc.).
3. **Plateforme** : Indiquez la plateforme (PS3, Xbox, PC, etc.).
4. **Année de sortie** : Sélectionnez l'année de sortie du jeu.
5. **Score Metacritic** : Entrez le score du jeu sur Metacritic.
6. **Score utilisateur** : Entrez le score des utilisateurs.

Cliquez ensuite sur **Prédire** pour voir les résultats des ventes globales prédits.
### Perception de mon produit
Découvrez ce que vos utilisateurs pensent de votre produit en téléchargeant un fichier CSV contenant des avis utilisateurs. Le fichier doit avoir une colonne unique appelée **`user_review`**, qui doit contenir les avis des utilisateurs en langue anglaise.
### Utilisation du fichier CSV

1. Téléchargez le fichier CSV à partir du lien ci-dessous.
2. Sur l'interface **Streamlit**, allez dans la section **Perception de mon produit**.
3. Chargez le fichier CSV via l'interface de téléchargement et laissez l'algorithme analyser les avis.

[**Téléchargez l'exemple CSV ici**](https://github.com/cedricNA/VideosGames_Sales_Predictions/blob/main/Data/df_test_avis_english_part_2.csv)

Le fichier **df_test_avis_english_part_2.csv** contient plusieurs avis utilisateurs en anglais et est structuré de la manière suivante :

```csv
user_review
"This game is amazing! I love the graphics and gameplay."
"The controls are a bit clunky, but the storyline is engaging."
"Terrible game. Too many bugs and glitches."
"One of the best RPGs I have ever played!"
```
## Dépendances
Le projet utilise les bibliothèques suivantes :
- **Streamlit** : Pour l'interface utilisateur interactive.
- **Scikit-learn**: Pour les modèles de prédiction.
- **Pandas**: Pour la manipulation des données.
- **Matplotlib** et Plotly : Pour les visualisations.
- **NLTK**: Pour l'analyse des avis utilisateurs.
  
## Limitation connue
- **Pygame** : Le projet inclut **2 jeux surprises** qui ne fonctionnent pas sur Streamlit Cloud car Streamlit ne supporte pas les interfaces graphiques natives. Si vous souhaitez jouer aux jeux , exécutez le projet en local.

## Déploiement

L'application est actuellement déployée sur **Streamlit Cloud** et accessible via ce lien :  
[https://videosgamessalespredictions.streamlit.app/](https://videosgamessalespredictions.streamlit.app/)

Pour déployer votre propre version :

1. **Créez un compte** sur [Streamlit Cloud](https://streamlit.io/cloud).
2. **Connectez votre dépôt GitHub** à Streamlit Cloud.
3. **Déployez l'application** en suivant les instructions fournies par Streamlit.



