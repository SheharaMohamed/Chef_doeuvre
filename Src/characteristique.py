from os import name
import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

import modules_emploi as me

def interface_characteristique(age, sexe,df):
   
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
        df_temp = df[(df.sexe.str.contains(sexe)) & (df.group_dage.str.contains(age))]

    elif (sexe == 'E') & (age != 'T'):
        df_temp = df[(df.group_dage.str.contains(age))].groupby(['année','characteristique']).sum().reset_index()

    elif (sexe != 'E') & (age == 'T'): 
        df_temp = df[(df.sexe.str.contains(sexe))].groupby(['année','characteristique']).sum().reset_index()

    else:
        df_temp = df.groupby(['année','characteristique']).sum().reset_index()

    if c != "Ensemble":
        display_df_temp = me.calc_percentage(df_temp[df_temp.characteristique == c],['nombre_employe'])
        display_df = df_temp[df_temp.characteristique == c]

        fig1 = px.line(display_df, x='année', y='nombre_employe') 
        fig2 = px.area(display_df_temp, x='année', y='perc_employe')

        fig1.update_layout(showlegend=False,
                        title_x=0.5,
                        xaxis_title='',
                        yaxis_title='Nombre d\'emploi (millier)',
                        width = 1400,
                        height = 400)
        fig1.update_xaxes(title_text="", row=1, col=2)          
        fig1.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
        # fig1.for_each_trace(lambda t: t.update(name=t.name.split("=")[1]))

        fig2.update_layout(showlegend=True,
                legend=dict(
                orientation="h",
                title = ''
                ),
                title_x=0.5,
                xaxis_title='Année',
                yaxis_title='Pourcentage',
                width = 1400,
                height = 400)
        fig2.update_xaxes(title_text="Année", row=1, col=2)
        fig2.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
     
    else:
        display_df_temp = me.calc_percentage(df_temp.groupby('année').sum().reset_index(),['nombre_employe'])
        display_df = df_temp

        fig1 = px.line(display_df, x='année', y=['nombre_employe'], color = 'characteristique')
        fig2 = px.area(display_df_temp, x='année', y='perc_employe')

        fig1.update_layout(showlegend=True,
                        legend=dict(
                            title = 'Groupe d\'age'
                        ),
                        title_x=0.5,
                        xaxis_title='',
                        yaxis_title='Nombre (en millier)',
                        width = 1400,
                        height = 400)
        fig1.update_xaxes(title_text="", row=1, col=2)
        fig1.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))

        fig2.update_layout(showlegend=True,
                legend=dict(
                orientation="h",
                title = ''
                ),
                title_x=0.5,
                xaxis_title='Année',
                yaxis_title='Pourcentage',
                width = 1400,
                height = 400)
        fig2.update_xaxes(title_text="Année", row=1, col=2)
        fig2.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))

    a = st.sidebar.slider(
        label = "Année",
        min_value = int(df.année.min()),
        max_value = int(df.année.max()),
        step = 1
    )

    dict_age = dict(zip(['T0','T15','T25','T50', "T"],["0 ans - 14 ans","15 ans - 24 ans", "25 ans - 50 ans", "50 ans et plus", "Ensemble"]))

    if c == 'Ensemble':
        df_temp =df.groupby(['année','group_dage','sexe']).sum().reset_index()
        df_temp = df_temp[df_temp.année == a]

    else:
        df_temp =df[df.characteristique == c]
        df_temp = df_temp[df_temp.année == a]

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

    b = st.sidebar.button('Backup')

    if b:
        me.backup(df,'data/indicateur_caratéristique')

    st.header("L'évolution annuelle d'emplois")
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)

    st.header("Nombre d'emploi de l'année {}".format(a))
    st.subheader("{} - {}".format(t,c))
    col_fig3, col_fig4 = st.columns((1,1))
    col_fig3.subheader("Par groupe d'age")
    col_fig3.plotly_chart(fig3)
    col_fig4.subheader("Part des hommes et des femmes")
    col_fig4.plotly_chart(fig4)