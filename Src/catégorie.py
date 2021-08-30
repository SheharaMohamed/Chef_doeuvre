from os import name
import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

import modules_emploi as me

def interface_catégorie(age, sexe,df):

    opts_cat = list(df['catégorie'].unique())
    opts_cat.append("Ensemble")

    c = st.sidebar.selectbox(
        "Catégorie",
        opts_cat
    )

    if (sexe != 'E') & (age != 'T'):
        df_temp = df[(df.sexe.str.contains(sexe)) & (df.group_dage.str.contains(age))]

    elif (sexe == 'E') & (age != 'T'):
        df_temp = df[(df.group_dage.str.contains(age))].groupby(['année','catégorie']).sum().reset_index()

    elif (sexe != 'E') & (age == 'T'): 
        df_temp = df[(df.sexe.str.contains(sexe))].groupby(['année','catégorie']).sum().reset_index()

    else:
        df_temp = df.groupby(['année','catégorie']).sum().reset_index()

    value_vars = ['nombre_employe','nombre_chomeur']
    value_vars_ = ['perc_employe','perc_chomeur']

    id_vars = df_temp.columns.tolist()[:-2]

    nm_dic = {'nombre_employe':"Nombre d'emplois", 'nombre_chomeur': "Nombre de chômeur"}
    nm_dic_ = {'perc_employe':"Pourcentage d'emplois", 'perc_chomeur': "Porcentage de chômeur"}

    if c != "Ensemble":
        display_df_temp = me.calc_percentage(df_temp[df_temp.catégorie == c],['nombre_employe','nombre_chomeur'])
        
        display_df_temp = pd.melt(display_df_temp, id_vars = id_vars, value_vars = value_vars_,
                        var_name = "type_de_nombre", value_name = "nombre")
        display_df = pd.melt(df_temp[df_temp.catégorie == c], id_vars = id_vars, value_vars = value_vars,
                        var_name = "type_de_nombre", value_name = "nombre")

        display_df['type_de_nombre'] = display_df['type_de_nombre'].apply(lambda x: nm_dic[x])
        display_df_temp['type_de_nombre'] = display_df_temp['type_de_nombre'].apply(lambda x: nm_dic_[x])

        fig1 = px.line(display_df, x='année', y='nombre', facet_col = "type_de_nombre")
        fig2 = px.area(display_df_temp, x='année', y='nombre', facet_col = "type_de_nombre" )

        fig1.update_layout(showlegend=False,
                        title_x=0.5,
                        xaxis_title='',
                        yaxis_title='Nombre (en millier)',
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
        display_df_temp = me.calc_percentage(df_temp.groupby('année').sum().reset_index(),['nombre_employe','nombre_chomeur'])   
        
        display_df_temp = pd.melt(display_df_temp, id_vars = ['année'], value_vars = value_vars_,
                        var_name = "type_de_nombre", value_name = "nombre")        
        display_df = pd.melt(df_temp, id_vars = id_vars, value_vars = value_vars,
                        var_name = "type_de_nombre", value_name = "nombre")  

        display_df['type_de_nombre'] = display_df['type_de_nombre'].apply(lambda x: nm_dic[x])
        display_df_temp['type_de_nombre'] = display_df_temp['type_de_nombre'].apply(lambda x: nm_dic_[x])

        fig1 = px.line(display_df, x='année', y=['nombre'], color = 'catégorie', facet_col = "type_de_nombre")
        fig2 = px.area(display_df_temp, x='année', y='nombre', facet_col = "type_de_nombre" )
    
    
        fig1.update_layout(showlegend=True,
                        legend=dict(
                        orientation="h",
                        title = ''
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
        df_temp =df[df.catégorie == c]
        df_temp = df_temp[df_temp.année == a]

    df_temp['group_dage'] = df_temp['group_dage'].apply(lambda x: dict_age[x])

    fig = px.line_polar(df[df.année == a].groupby('catégorie').sum().reset_index(), r='nombre_employe', theta='catégorie', line_close=True)
    fig.update_traces(fill='toself')

    fig_ = px.line_polar(df[df.année == a].groupby('catégorie').sum().reset_index(), r='nombre_chomeur', theta='catégorie', line_close=True)
    fig_.update_traces(fill='toself')

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

    b = st.sidebar.button('Backup')

    if b:
        me.backup(df,'data/indicateur_catégorie')

    st.header("L'evolution annuelle des emplois et des chomeurs")
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)
    
    col_fig, col_fig_ = st.columns((1,1))
    col_fig.subheader("La distribution des emplois")
    col_fig.plotly_chart(fig)
    col_fig_.subheader("La distribution des chômeurs")
    col_fig_.plotly_chart(fig_)

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