from os import name
import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

from sqlalchemy import create_engine

def interface_characteristique(age, sexe):

    # Création d'engine pour connecter le serveur MySQL
    engine = create_engine(
    "mysql+pymysql://root:tashe1129@localhost/emploi?charset=utf8mb4&binary_prefix=true")
    
    # Définir la connection pour la base de donnée
    conn = engine.connect()

    #Définir differentes types de reqûtes SQL
    q = '''SELECT c.characteristique, p.*, t.* FROM année a
	        INNER JOIN (SELECT * FROM population INNER JOIN indicateur_chardemploi USING (pop_id)) p USING (année)
            INNER JOIN char_demploi c USING (cha_id)
            INNER JOIN type_char t USING (typ_id)
            ORDER BY p.année;'''

    df_main = pd.read_sql(q,conn)

    #Une copie pour utilisé actuellement
    df = pd.read_sql(q, conn)
    df_main = df_main[df_main.année >= 1982]
    df = df[df.année >= 1982]

    #Ajouter les choix de la characteristique    
    opts_typ = list(df['type_characteristique'].unique())
    
    t = st.sidebar.selectbox(
        "Type",
        opts_typ
    )

    if t == 'Sous-emploi':
        opts_char = list(df[df.type_characteristique.str.contains(t)]['characteristique'].unique())
        opts_char.append("Ensemble")
        c = st.sidebar.selectbox(
            "Characteristique",
            opts_char
        )
    elif t == 'Temp de travail':
        opts_char = list(df[df.type_characteristique.str.contains(t)]['characteristique'].unique())
        opts_char.append("Ensemble")
        c = st.sidebar.selectbox(
            "Characteristique",
            opts_char
        )
    else:
        opts_char = list(df[df.type_characteristique.str.contains(t)]['characteristique'].unique())
        opts_char.append("Ensemble")
        c = st.sidebar.selectbox(
            "Characteristique",
            opts_char
        )

    if (sexe != 'E') & (age != 'T'):
        df = df[(df.sexe.str.contains(sexe)) & (df.group_dage.str.contains(age))]

    elif (sexe == 'E') & (age != 'T'):
        df = df[(df.group_dage.str.contains(age))].groupby(['année','characteristique']).sum().reset_index()

    elif (sexe != 'E') & (age == 'T'): 
        df = df[(df.sexe.str.contains(sexe))].groupby(['année','characteristique']).sum().reset_index()

    else:
        df = df.groupby(['année','characteristique']).sum().reset_index()

    conn.close()
    

    if c != "Ensemble":
        
        display_df = df[df.characteristique == c]
        fig1 = px.line(display_df, x='année', y='nombre_employe') 

        fig1.update_layout(showlegend=False,
                        title_x=0.5,
                        xaxis_title='année',
                        yaxis_title='Nombre d\'emploi (millier)',
                        width = 1400,
                        height = 400)
                        
        fig1.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
        # fig1.for_each_trace(lambda t: t.update(name=t.name.split("=")[1]))
     
    else:
        
        display_df = df 
        fig1 = px.line(display_df, x='année', y=['nombre_employe'], color = 'characteristique')
   
        fig1.update_layout(showlegend=True,
                        legend=dict(
                            title = 'Groupe d\'age'
                        ),
                        title_x=0.5,
                        xaxis_title='année',
                        yaxis_title='Nombre (millier)',
                        width = 1400,
                        height = 400)
        fig1.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))

    a = st.sidebar.slider(
        label = "Année",
        min_value = int(df.année.min()),
        max_value = int(df.année.max()),
        step = 1
    )

    dict_age = dict(zip(['T0','T15','T25','T50', "T"],["0 ans - 14 ans","15 ans - 24 ans", "25 ans - 50 ans", "50 ans et plus", "Ensemble"]))

    if c == 'Ensemble':
        df_temp =df_main

    else:
        df_temp =df_main[df_main.characteristique == c]

    df_temp['group_dage'] = df_temp['group_dage'].apply(lambda x: dict_age[x])

    fig3 = px.bar(df_temp, x="sexe", y="nombre_employe",
             color='group_dage', barmode='group')

    fig3.update_layout(showlegend = True,
                        legend=dict(
                            title = 'Groupe d\'age'
                        ),
                        title_x=0.5,
                        xaxis_title='sexe',
                        yaxis_title='Nombre d\'emploi (millier)')
    fig3.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
    
    fig4 = px.pie(df_temp, names = 'sexe', values = 'nombre_employe')

    fig4.update_layout(showlegend = True,
                            legend = dict(
                                title = 'Sexe'
                            ))

    st.header("L'evolution annuelle des emplois")
    st.plotly_chart(fig1)

    st.header("Nombre d'emploi de l'année {}".format(a))
    col_fig3, col_fig4 = st.columns((1,1))
    col_fig3.subheader("Par groupe d'age")
    col_fig3.plotly_chart(fig3)
    col_fig4.subheader("Part des hommes et des femmes")
    col_fig4.plotly_chart(fig4)