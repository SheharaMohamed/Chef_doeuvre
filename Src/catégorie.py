from os import name
import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

from sqlalchemy import create_engine

def interface_catégorie(age, sexe):

    # Création d'engine pour connecter le serveur MySQL
    engine = create_engine(
    "mysql+pymysql://root:tashe1129@localhost/emploi?charset=utf8mb4&binary_prefix=true")
    
    # Définir la connection pour la base de donnée
    conn = engine.connect()

    #Définir differentes types de reqûtes SQL
    q = '''SELECT c.catégorie, p.* FROM année a
	        INNER JOIN (SELECT * FROM population INNER JOIN indicateur_catégorie USING (pop_id)) p USING (année)
            INNER JOIN catégorie c USING (cat_id)
            ORDER BY p.année;'''

    df_main = pd.read_sql(q,conn)

    #Une copie pour utilisé actuellement
    df = pd.read_sql(q, conn)

    #Ajouter les choix de dipôme
    opts_cat = list(df['catégorie'].unique())
    opts_cat.append("Ensemble")

    c = st.sidebar.selectbox(
        "Catégorie",
        opts_cat
    )

    if (sexe != 'E') & (age != 'T'):
        df = df[(df.sexe.str.contains(sexe)) & (df.group_dage.str.contains(age))]

    elif (sexe == 'E') & (age != 'T'):
        df = df[(df.group_dage.str.contains(age))].groupby(['année','catégorie']).sum().reset_index()

    elif (sexe != 'E') & (age == 'T'): 
        df = df[(df.sexe.str.contains(sexe))].groupby(['année','catégorie']).sum().reset_index()

    else:
        df = df.groupby(['année','catégorie']).sum().reset_index()

    conn.close()
    

    value_vars = ['nombre_employe','nombre_chomeur']
    id_vars = df.columns.tolist()[:-2]

    if c != "Ensemble":
        
        display_df = pd.melt(df[df.catégorie == c], id_vars = id_vars, value_vars = value_vars,
                        var_name = "type_de_nombre", value_name = "nombre")
        fig1 = px.line(display_df, x='année', y='nombre', facet_col = "type_de_nombre")
        # fig2 = px.line(display_df, x='année', y=['nombre_chomeur'])  

        fig1.update_layout(showlegend=False,
                        title_x=0.5,
                        xaxis_title='année',
                        yaxis_title='Nombre (millier)',
                        width = 1400,
                        height = 400)
        fig1.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
        # fig1.for_each_trace(lambda t: t.update(name=t.name.split("=")[1]))
     
    else:
        
        display_df = pd.melt(df, id_vars = id_vars, value_vars = value_vars,
                        var_name = "type_de_nombre", value_name = "nombre")  
        fig1 = px.line(display_df, x='année', y=['nombre'], color = 'catégorie', facet_col = "type_de_nombre")
        # fig2 = px.line(display_df, x='année', y=['nombre_chomeur'], color = 'catégorie')
    
    
        fig1.update_layout(showlegend=True,
                        legend=dict(
                        orientation="h",
                        title = ''
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
        df_temp =df_main[df_main.catégorie == c]

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

    fig5 = px.bar(df_temp, x="sexe", y="nombre_chomeur",
            color='group_dage', barmode='group')

    fig5.update_layout(showlegend = True,
                        legend=dict(
                        title = 'Groupe d\'age'
                        ),
                        title_x=0.5,
                        xaxis_title='sexe',
                        yaxis_title='Nombre de chomeur (millier)')

    fig5.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
    
    fig6 = px.pie(df_temp, names = 'sexe', values = 'nombre_chomeur')
    
    fig6.update_layout(showlegend = True,
                        legend = dict(
                            title = 'Sexe'
                        ))

    st.header("L'evolution annuelle des emplois et des chomeurs")
    st.plotly_chart(fig1)

    st.header("Nombre d'emploi de l'année {}".format(a))
    col_fig3, col_fig4 = st.columns((1,1))
    col_fig3.subheader("Par groupe d'age")
    col_fig3.plotly_chart(fig3)
    col_fig4.subheader("Part des hommes et des femmes")
    col_fig4.plotly_chart(fig4)

    st.header("Nombre de chomeur de l'année {}".format(a))
    col_fig5, col_fig6 = st.columns((1,1))    
    col_fig5.subheader("Par groupe d'age")
    col_fig5.plotly_chart(fig5)
    col_fig6.subheader("Part des hommes et des femmes")
    col_fig6.plotly_chart(fig6)