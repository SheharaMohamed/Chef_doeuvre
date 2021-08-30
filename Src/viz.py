import streamlit as st
import pandas as pd
import numpy as np
import diplôme
import catégorie
import characteristique
import géographique
import ensemble
import globals

from sqlalchemy import create_engine

import pymysql

st.set_page_config(layout="wide")

nav = st.sidebar.radio(
    "Choisissez l'indicateur",
    ["Ensemble", "Diplôme", "Catégorie Socioprofessionnelle", "Caractéristique d'emploi", "Le secteur géographique"]
)

engine = create_engine("mysql+pymysql://user1:mdp1@localhost/emploi?charset=utf8mb4&binary_prefix=true")

sexe = dict(zip(["Femme", "Homme", "Ensemble"],['F','H','E']))
age = dict(zip(["0 ans - 14 ans","15 ans - 24 ans", "25 ans - 50 ans", "50 ans et plus", "Ensemble"],['T0','T15','T25','T50', "T"]))

if nav == "Diplôme":
    s = st.sidebar.selectbox(
    "Sexe",
    ["Femme", "Homme", "Ensemble"],
    index = 0
    )
    g = st.sidebar.selectbox(
            "Groupe d'age",
            ["15 ans - 24 ans", "25 ans - 50 ans", "50 ans et plus", "Ensemble"],
            index = 1
            )
    st.title("Comparateur d'emploi par diplôme")
    diplôme.interface_diplôme(age[g],sexe[s],globals.df_dip)

elif nav == "Catégorie Socioprofessionnelle":
    s = st.sidebar.selectbox(
    "Sexe",
    ["Femme", "Homme", "Ensemble"],
    index = 0
    )
    g = st.sidebar.selectbox(
            "Groupe d'age",
            ["15 ans - 24 ans", "25 ans - 50 ans", "50 ans et plus", "Ensemble"],
            index = 1
            )
    st.title("Comparateur d'emploi par catégorie socioprofessionnelle")
    catégorie.interface_catégorie(age[g],sexe[s],globals.df_cat)

elif nav == "Caractéristique d'emploi":
    s = st.sidebar.selectbox(
    "Sexe",
    ["Femme", "Homme", "Ensemble"],
    index = 0
    )
    g = st.sidebar.selectbox(
            "Groupe d'age",
            ["15 ans - 24 ans", "25 ans - 50 ans", "50 ans et plus", "Ensemble"],
            index = 1
            )
    st.title("Comparateur d'emploi par caractéristique d'emploi")
    characteristique.interface_characteristique(age[g],sexe[s],globals.df_cha)

elif nav == "Le secteur géographique":
    s = st.sidebar.selectbox(
    "Sexe",
    ["Femme", "Homme", "Ensemble"],
    index = 0
    )
    g = st.sidebar.selectbox(
            "Groupe d'age",
            ["0 ans - 14 ans","15 ans - 24 ans", "25 ans - 50 ans", "50 ans et plus", "Ensemble"],
            index = 1
            )
    st.title("Comparateur d'emploi par le secteur géographique")
    géographique.interface_géographique(age[g], sexe[s], globals.df_geo)

else:
    st.title("L'évolution d'emplois et de chômeurs en France")
    ensemble.interface_ensemble(globals.df_dip, globals.df_cat, globals.df_cha, globals.df_geo)

