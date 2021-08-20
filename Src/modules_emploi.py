from sqlalchemy import create_engine
import pymysql

import streamlit as st

# Création d'engine pour connecter le serveur MySQL
engine = create_engine(
"mysql+pymysql://root:tashe1129@localhost/emploi?charset=utf8mb4&binary_prefix=true")

# Définir la connection pour la base de donnée
conn = engine.connect()

def exec():
    q = "SELECT * FROM diplôme;"
    res = conn.execute(q)
    for el in res:
        st.write(el)