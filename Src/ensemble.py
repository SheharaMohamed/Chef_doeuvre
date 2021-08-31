import streamlit as st
from streamlit_metrics import metric, metric_row
import pandas as pd
import numpy as np
import geopandas as gpd

from streamlit_folium import folium_static
import folium

import plotly.express as px
import plotly.graph_objects as go

import modules_emploi as me

def interface_ensemble(df_dip, df_cat, df_cha, df_geo):

    a = st.sidebar.slider(
        label = "Année",
        min_value = int(df_dip.année.min()),
        max_value = int(df_dip.année.max()),
        step = 1
    )
    df_temp1 = df_geo[df_geo.group_dage != 'T0'].groupby('année').sum().reset_index()[['année', 'population']]
    df_temp2 = df_dip.groupby('année').sum().reset_index()[['année', 'nombre_employe', 'nombre_chomeur']]
    df_temp = pd.merge(df_temp2,df_temp1, left_on='année',right_on='année')
    df_temp['population'] = df_temp['population']/1000
    df_temp['nombre_retraite'] = df_temp['population']*0.3

    df_temp_ = pd.melt(df_temp, id_vars = ['année'], value_vars = df_temp.columns.tolist()[1:])
    
    l = df_temp[df_temp.année == a]
    pop = round(l.population.iloc[0],2)
    emp = round(l.nombre_employe.iloc[0],2)
    cho = round(l.nombre_chomeur.iloc[0],2)
    ret = round(l.nombre_retraite.iloc[0],2)
    pop_ac = round(emp+cho,2)  
    pop_na = pop - pop_ac - ret  

    dict_pop = dict(zip(['nombre_employe','nombre_chomeur','population','nombre_retraite'],
                        ["Nombre d'emplois","Nombre de chômeurs", "Population", "Retraites"]))
    df_temp_.variable = df_temp_.variable.apply(lambda x: dict_pop[x])

    fig1 = px.line(df_temp_, x = 'année', y = 'value', color = 'variable')

    fig1.update_layout(showlegend=True,
                    legend=dict(
                        title = 'Type de population'
                    ),
                    title_x=0.5,
                    xaxis_title='Année',
                    yaxis_title='Nombre (en millier)',
                    width = 900,
                    height = 400)
    fig1.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))

    dict_age = dict(zip(['T0','T15','T25','T50', "T"],["0 ans - 14 ans","15 ans - 24 ans", "25 ans - 50 ans", "50 ans et plus", "Ensemble"]))

    tmp = pd.DataFrame({'values' : [pop_na, emp, cho, ret],
                        'names' : ["Population non active","Population avec emploi", "Chômeurs", "Retraites"]})

    df_temp_group = df_dip[df_dip.année == a].groupby(['année','group_dage','sexe']).sum().reset_index()
    df_temp_group['group_dage'] = df_temp_group['group_dage'].apply(lambda x: dict_age[x])
    df_temp_dip = df_dip[df_dip.année == a].groupby(['année','diplôme']).sum().reset_index()
    df_temp_cat = df_cat[df_cat.année == a].groupby(['année','catégorie','sexe']).sum().reset_index()
    df_temp_cha = df_cha[(df_cha.année == a) & (df_cha.characteristique.str.contains('Temp'))].groupby(['année','characteristique','sexe']).sum().reset_index()
    df_geodep_temp = df_geo[df_geo.année == a].groupby(['année','departement','code_postal']).sum().reset_index()
    df_georeg_temp = df_geo[df_geo.année == a].groupby(['année','region','code_reg']).sum().reset_index()
    
    geo_dep = r"https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements-avec-outre-mer.geojson"
    geo_reg = r"https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions-avec-outre-mer.geojson"
    geo_dep = gpd.read_file(geo_dep)
    geo_reg = gpd.read_file(geo_reg)

    df_geodep_temp = geo_dep.merge(df_geodep_temp, left_on = 'code', right_on = 'code_postal')
    df_georeg_temp = geo_reg.merge(df_georeg_temp, left_on = 'code', right_on = 'code_reg')

    fig2 = px.pie(tmp, names = 'names', values = 'values')

    fig3 = px.bar(df_temp_group, x = 'sexe', y = 'nombre_employe', color = 'group_dage', barmode='group')
    fig3.update_layout(showlegend = True,
                    legend=dict(
                    title = 'Groupe d\'age'
                    ),
                    title_x=0.5,
                    xaxis_title='sexe',
                    yaxis_title='Nombre d\'emploi (millier)')

    fig4 = px.line_polar(df_temp_dip, r='nombre_employe', theta='diplôme', line_close=True)
    fig4.update_traces(fill='toself')

    fig5 = px.bar(df_temp_cat, x = 'nombre_employe', y = 'catégorie', color = 'sexe', barmode='group')
    fig5.update_layout(
                    title_x=0.5,
                    xaxis_title='Nombre d\'emploi (millier)',
                    yaxis_title='Catégorie')

    fig6 = px.bar(df_temp_cha, y = 'nombre_employe', x = 'characteristique', color = 'sexe', barmode='group')
    fig6.update_layout(
                    title_x=0.5,
                    xaxis_title='Temp de travail',
                    yaxis_title='Nombre d\'emploi (millier)')
    
    #Les cartes
    m_cho_dep = folium.Map(location=[46.71109 ,1.7191036], zoom_start=5)

    folium.Choropleth(
        geo_data=df_geodep_temp,
        name="choropleth",
        data=df_geodep_temp,
        columns=["code_postal","nombre_chomeur"],
        key_on="feature.properties."+"code_postal",
        threshold_scales = "nombre_chomeur",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=.1,
        legend_name="",
    ).add_to(m_cho_dep).geojson.add_child(
        folium.features.GeoJsonTooltip(fields = ["departement", 'nombre_chomeur'])
    )

    m_cho_reg = folium.Map(location=[46.71109 ,1.7191036], zoom_start=5)

    folium.Choropleth(
        geo_data=df_georeg_temp,
        name="choropleth",
        data=df_georeg_temp,
        columns=["code_reg","nombre_chomeur"],
        key_on="feature.properties."+"code_reg",
        threshold_scales = "nombre_chomeur",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=.1,
        legend_name="",
    ).add_to(m_cho_reg).geojson.add_child(
        folium.features.GeoJsonTooltip(fields = ["region", 'nombre_chomeur'])
    )


    metric(
            "Année", a
        )

    
    col_tik1, col_tik2, col_tik3, col_tik4, col_tik5 = st.columns((1,1,1,1,1))
    
    with(col_tik1):
        metric(
            "Population eligible à travailler", str(pop)+'K'
        )
    with(col_tik2):
        metric(
            "Population active", str(pop_ac)+'K'
        )
    with(col_tik3):
        metric(
            "Nombre de chômeurs", str(cho)+'K'
        )
    with(col_tik4):
        metric(
            "Taux d'emplois", str(round(emp*100/pop,2))+'%'
        )
    with(col_tik5):
        metric(
            "Taux de chômeurs", str(round(cho*100/(pop_ac),2))+'%'
        )

    col_fig1, col_fig2 = st.columns((1.5,1))

    col_fig1.subheader("L'évolution de la population active et non active")
    col_fig1.plotly_chart(fig1)

    col_fig2.subheader("Les propotions de la population active en {}".format(a))
    col_fig2.plotly_chart(fig2)

    col_fig3, col_fig4 = st.columns((1.5,1))

    col_fig3.subheader("L'emploi par le groupe d'age et le sexe")
    col_fig3.plotly_chart(fig3)

    col_fig4.subheader("L'emploi par diplôme")
    col_fig4.plotly_chart(fig4)
    
    col_fig5, col_fig6 = st.columns((1.5,1))

    col_fig5.subheader("L'emploi par les catégories socioprofessionelle")
    col_fig5.plotly_chart(fig5)

    col_fig6.subheader("L'emploi par temps de travail")
    col_fig6.plotly_chart(fig6)

    col_geo, col_folium = st.columns((0.5,2))
    
    geo = col_geo.radio(
    "Choisissez le secteur géographique",
    ["Par département", "Par région"]
    )

    if geo == "Par département":
        with(col_folium):
            if (a < 2020) &  (a> 2013):
                st.subheader("Données indisponible pour l'année {}".format(a))
            else:
                st.subheader("Les chômeur par département")
                folium_static(m_cho_dep)
    else:
        with(col_folium):
            if (a < 2020) &  (a> 2013):
                st.subheader("Données indisponible pour l'année {}".format(a))
            else:
                st.subheader("Les chômeur par région")
                folium_static(m_cho_reg)
        
