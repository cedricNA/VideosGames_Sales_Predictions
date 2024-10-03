import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def dataviz():
    df = pd.read_csv("Data/Ventes_jeux_video_final.csv")

    df = df.dropna(axis=0)

    df["Year"] = df["Year"].astype(str)
    df["Year"] = df["Year"].str[:-2]
    df["Year"] = pd.to_datetime(df["Year"], format="%Y")
    df["Year"] = df["Year"].dt.year

    # Charger vos données (assurez-vous que df est défini dans votre environnement)
    # df = pd.read_csv('your_dataset.csv')  # Remplacer par le chargement réel de vos données

    st.title("📊 Page de DataViz 🎮")

    # Section: Distribution des ventes globales par genre de jeu
    st.header("Distribution des ventes globales par genre de jeu")
    fig1 = px.box(
        df,
        x="Genre",
        y="Global_Sales",
        color="Genre",
        title="Distribution des ventes globales par genre de jeu",
        labels={"Global_Sales": "Ventes globales (en millions)", "Genre": "Genre"},
        notched=True,
        points="all",
    )
    fig1.update_layout(
        xaxis_title="Genre",
        yaxis_title="Ventes globales (en millions)",
        xaxis_tickangle=45,
        yaxis=dict(type="log", autorange=True),
    )
    st.plotly_chart(fig1)

    # Section: Évolution des ventes globales par année
    st.header("Évolution des ventes globales par année")
    sales_by_year = df.groupby("Year")["Global_Sales"].sum()
    mean_sales = sales_by_year.mean()
    median_sales = sales_by_year.median()
    fig2 = go.Figure()
    fig2.add_trace(
        go.Scatter(
            x=sales_by_year.index,
            y=sales_by_year,
            mode="lines+markers",
            name="Ventes annuelles",
            line=dict(color="blue"),
        )
    )
    fig2.add_hline(
        y=mean_sales,
        line=dict(color="red", dash="solid"),
        annotation_text=f"Moyenne des ventes: {mean_sales:.2f} millions",
        annotation_position="bottom right",
    )
    fig2.add_hline(
        y=median_sales,
        line=dict(color="yellow", dash="dash"),
        annotation_text=f"Médiane des ventes: {median_sales:.2f} millions",
        annotation_position="bottom right",
    )
    fig2.update_layout(
        title="Évolution des ventes globales par année",
        xaxis_title="Année",
        yaxis_title="Ventes globales (en millions)",
        legend_title="Légende",
        width=1400,
        height=800,
    )
    st.plotly_chart(fig2)

    # Section: Ventes totales par régions
    st.header("Ventes totales par régions")
    region_sales = (
        df[["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"]].sum().reset_index()
    )
    region_sales.columns = ["Region", "Total_Sales"]
    fig3 = px.bar(
        region_sales,
        x="Region",
        y="Total_Sales",
        title="Ventes totales par Régions",
        labels={"Total_Sales": "Ventes totales (en millions)", "Region": "Région"},
        color="Total_Sales",
    )
    fig3.update_layout(
        xaxis_title="Régions",
        yaxis_title="Ventes totales (en millions)",
        xaxis_tickangle=-45,
    )
    st.plotly_chart(fig3)

    # Section: Ventes par région pour les 10 principaux éditeurs
    st.header("Ventes par région pour les 10 principaux éditeurs")
    ventes_par_editeur = (
        df.groupby("Publisher")
        .agg(
            {
                "Global_Sales": "sum",
                "NA_Sales": "sum",
                "EU_Sales": "sum",
                "JP_Sales": "sum",
                "Other_Sales": "sum",
            }
        )
        .reset_index()
    )
    top_editeurs = ventes_par_editeur.sort_values(
        by="Global_Sales", ascending=False
    ).head(10)
    ventes_top_editeurs = top_editeurs.melt(
        id_vars="Publisher",
        value_vars=["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"],
        var_name="Region",
        value_name="Sales",
    )
    fig5 = px.bar(
        ventes_top_editeurs,
        x="Publisher",
        y="Sales",
        color="Region",
        title="Ventes par région pour les 10 principaux éditeurs",
        labels={"Sales": "Ventes (en millions)", "Publisher": "Éditeur"},
        text_auto=True,
    )
    st.plotly_chart(fig5)

    # Section: Évolution des ventes par région
    st.header("Évolution des ventes par région")
    df_sales_year = df.groupby(["Year"]).agg(
        {"EU_Sales": "sum", "NA_Sales": "sum", "JP_Sales": "sum", "Other_Sales": "sum"}
    )
    fig6 = px.bar(
        df_sales_year,
        x=df_sales_year.index,
        y=["NA_Sales", "EU_Sales", "JP_Sales", "Other_Sales"],
        title="Evolution des ventes par région",
    )
    fig6.update_layout(
        xaxis_title="Années", yaxis_title="Ventes par régions(en millions)"
    )
    st.plotly_chart(fig6)

    # Section: Relation entre les ventes régionales et les ventes globales
    st.header("Relation entre les ventes régionales et les ventes globales")
    fig, axes = plt.subplots(2, 2, figsize=(18, 12))
    fig.suptitle("Relation entre les ventes régionales et les ventes globales")

    # Ventes en Amérique du Nord vs Ventes Globales
    sns.scatterplot(
        ax=axes[0, 0],
        data=df,
        x="NA_Sales",
        y="Global_Sales",
        hue="Genre",
        style="Genre",
        s=100,
    )
    axes[0, 0].set_title("Ventes NA vs Ventes Globales")
    axes[0, 0].set_xlabel("Ventes NA (en millions)")
    axes[0, 0].set_ylabel("Ventes Globales (en millions)")

    # Ventes en Europe vs Ventes Globales
    sns.scatterplot(
        ax=axes[0, 1],
        data=df,
        x="EU_Sales",
        y="Global_Sales",
        hue="Genre",
        style="Genre",
        s=100,
    )
    axes[0, 1].set_title("Ventes EU vs Ventes Globales")
    axes[0, 1].set_xlabel("Ventes EU (en millions)")
    axes[0, 1].set_ylabel("Ventes Globales (en millions)")

    # Ventes au Japon vs Ventes Globales
    sns.scatterplot(
        ax=axes[1, 0],
        data=df,
        x="JP_Sales",
        y="Global_Sales",
        hue="Genre",
        style="Genre",
        s=100,
    )
    axes[1, 0].set_title("Ventes JP vs Ventes Globales")
    axes[1, 0].set_xlabel("Ventes JP (en millions)")
    axes[1, 0].set_ylabel("Ventes Globales (en millions)")

    # Autres ventes vs Ventes Globales
    sns.scatterplot(
        ax=axes[1, 1],
        data=df,
        x="Other_Sales",
        y="Global_Sales",
        hue="Genre",
        style="Genre",
        s=100,
    )
    axes[1, 1].set_title("Autres Ventes vs Ventes Globales")
    axes[1, 1].set_xlabel("Autres Ventes (en millions)")
    axes[1, 1].set_ylabel("Ventes Globales (en millions)")

    st.pyplot(fig)

    # Section: Corrélation entre les ventes globales et les ventes de jeux de différents genres
    st.header(
        "Corrélation entre les ventes globales et les ventes de jeux de différents genres"
    )

    # Filtrer les données pour les top 5 genres
    top_5_genre = ["Sports", "Action", "Role-Playing", "Shooter", "Platform"]
    df_top_5_genre = df[df["Genre"].isin(top_5_genre)]

    # Créer un tableau croisé dynamique pour obtenir les ventes globales par année et par genre
    df_top_5_genre = df_top_5_genre.pivot_table(
        values="Global_Sales", index="Year", columns="Genre", aggfunc="sum"
    ).fillna(0)
    df_top_5_genre["Global_Sales"] = df_top_5_genre.sum(axis=1)

    fig.show()
    # Créer les scatter plots
    fig1 = px.scatter(
        df_top_5_genre,
        x="Action",
        y="Global_Sales",
        trendline="ols",
        trendline_scope="trace",
        trendline_color_override="red",
        title="Corrélation entre les ventes globales et les ventes de jeux de type Action",
    )
    fig2 = px.scatter(
        df_top_5_genre,
        x="Shooter",
        y="Global_Sales",
        trendline="ols",
        trendline_scope="trace",
        trendline_color_override="red",
        title="Corrélation entre les ventes globales et les ventes de jeux de type Shooter",
    )
    fig3 = px.scatter(
        df_top_5_genre,
        x="Role-Playing",
        y="Global_Sales",
        trendline="ols",
        trendline_scope="trace",
        trendline_color_override="red",
        title="Corrélation entre les ventes globales et les ventes de jeux de type Role-Playing",
    )
    fig4 = px.scatter(
        df_top_5_genre,
        x="Sports",
        y="Global_Sales",
        trendline="ols",
        trendline_scope="trace",
        trendline_color_override="red",
        title="Corrélation entre les ventes globales et les ventes de jeux de type Sports",
    )
    fig5 = px.scatter(
        df_top_5_genre,
        x="Platform",
        y="Global_Sales",
        trendline="ols",
        trendline_scope="trace",
        trendline_color_override="red",
        title="Corrélation entre les ventes globales et les ventes de jeux de type Platform",
    )

    # Afficher les scatter plots dans Streamlit un par un
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)
    st.plotly_chart(fig3)
    st.plotly_chart(fig4)
    st.plotly_chart(fig5)

    # Créer le graphique à barres empilées
    fig = px.bar(
        df_top_5_genre,
        x=df_top_5_genre.index,
        y=df_top_5_genre.columns,
        title="Évolution des ventes en fonction des genres",
    )

    # Mettre à jour les labels des axes
    fig.update_layout(xaxis_title="Années", yaxis_title="Ventes globales (en millions)")
    st.plotly_chart(fig)

    # Section: Corrélation entre meta_score et user_review
    st.header("Corrélation entre Meta Score et User Review")
    scatter_meta_user = px.scatter(
        df,
        x="meta_score",
        y="user_review",
        title="Relation entre Meta Score et User Review",
        labels={"meta_score": "Meta Score", "user_review": "User Review"},
        trendline="ols",
    )
    st.plotly_chart(scatter_meta_user)

    # Hist des ventes globales en fonction du score Meta
    st.header("Ventes globales en fonction du score Meta")
    hist_meta_sales = px.histogram(
        df,
        x="meta_score",
        y="Global_Sales",
        title="Ventes globales en fonction du score Meta",
        labels={
            "meta_score": "Meta Score",
            "Global_Sales": "Ventes globales (en millions)",
        },
        log_y=True,
    )
    st.plotly_chart(hist_meta_sales)

    # Hist des ventes globales en fonction des notes utilisateurs
    st.header("Ventes globales en fonction des notes utilisateurs")
    hist_user_sales = px.histogram(
        df,
        x="user_review",
        y="Global_Sales",
        color_discrete_sequence=["red"],
        title="Ventes globales en fonction des notes utilisateurs",
        labels={
            "user_review": "User Review",
            "Global_Sales": "Ventes globales (en millions)",
        },
        log_y=True,
    )
    st.plotly_chart(hist_user_sales)

    # Section: Médianes des avis des joueurs et de la presse en fonction des genres de jeu
    st.header(
        "Médiane des avis des joueurs et de la presse en fonction des genres de jeu"
    )
    df_score = df.groupby(["Genre"]).agg({"user_review": "mean", "meta_score": "mean"})
    df_score = df_score.sort_values("user_review")

    # Histogramme des avis des joueurs par genre
    hist_user_genre = px.histogram(
        df_score,
        x=df_score.index,
        y="user_review",
        color=df_score.index,
        title="Médiane des avis des joueurs en fonction des genres de jeu",
        labels={"user_review": "Avis des joueurs"},
    )
    hist_user_genre.update_layout(yaxis_title="Avis des joueurs")
    hist_user_genre.update_yaxes(range=[7.1, 8])
    st.plotly_chart(hist_user_genre)

    # Histogramme des avis de la presse par genre
    df_score = df_score.sort_values("meta_score")
    hist_meta_genre = px.histogram(
        df_score,
        x=df_score.index,
        y="meta_score",
        color=df_score.index,
        title="Médiane des avis de presse en fonction des genres de jeu",
        labels={"meta_score": "Avis de la presse"},
    )
    hist_meta_genre.update_layout(yaxis_title="Avis de la presse")
    hist_meta_genre.update_yaxes(range=[68, 80])
    st.plotly_chart(hist_meta_genre)
