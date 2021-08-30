import streamlit as st

from streamlit_folium import folium_static
import folium

import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import numpy as np
import geopandas as gpd

import modules_emploi as me

"# streamlit-folium"

def interface_géographique(age, sexe, df):
            
    #Selection d'année
    a = st.sidebar.slider(
        label = "Année",
        min_value = 2013,
        max_value = int(df.année.max()),
        step = 1
    )

    geo = st.sidebar.radio(
        "Choissiez le niveau géographie", 
        ['Départemental', 'Régionale']
    )


    #Lire les fichiers géographique des départements et des régions
    geo_dep = r"https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements-avec-outre-mer.geojson"
    geo_reg = r"https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions-avec-outre-mer.geojson"

    #Utiliser geopandas pour decoder le fichier json
    geo_dep = gpd.read_file(geo_dep)
    geo_reg = gpd.read_file(geo_reg)
    
    if (sexe != 'E') & (age != 'T'):
        temp_dep = df[(df.sexe == sexe) & (df.group_dage == age)].groupby(['année','code_postal','departement']).sum().reset_index()
        temp_reg = df[(df.sexe == sexe) & (df.group_dage == age)].groupby(['année','code_reg','region']).sum().reset_index()

        sal_dep =  df[(df.sexe == sexe) & (df.group_dage == age)].groupby(['année','code_postal','departement']).mean().reset_index()
        sal_reg =  df[(df.sexe == sexe) & (df.group_dage == age)].groupby(['année','code_reg','region']).mean().reset_index()

    elif (sexe == 'E') & (age != 'T'):
        temp_dep = df[(df.group_dage == age)].groupby(['année','code_postal','departement']).sum().reset_index()
        temp_reg = df[(df.group_dage == age)].groupby(['année','code_reg','region']).sum().reset_index()

        sal_dep =  df[(df.group_dage == age)].groupby(['année','code_postal','departement']).mean().reset_index()
        sal_reg =  df[(df.group_dage == age)].groupby(['année','code_reg','region']).mean().reset_index()

    elif (sexe != 'E') & (age == 'T'): 
        temp_dep = df[(df.sexe == sexe)].groupby(['année','code_postal','departement']).sum().reset_index()
        temp_reg = df[(df.sexe == sexe)].groupby(['année','code_reg','region']).sum().reset_index()

        sal_dep =  df[(df.sexe == sexe)].groupby(['année','code_postal','departement']).mean().reset_index()
        sal_reg =  df[(df.sexe == sexe)].groupby(['année','code_reg','region']).mean().reset_index()

    else:
        temp_dep = df.groupby(['année','code_postal','departement']).sum().reset_index()
        temp_reg = df.groupby(['année','code_reg','region']).sum().reset_index()

        sal_dep =  df.groupby(['année','code_postal','departement']).sum().reset_index()
        sal_reg =  df.groupby(['année','code_reg','region']).sum().reset_index()


    #Concatener le dataframe avec données geographique
    code = ""
    nom = ""

    if geo == 'Départemental':
        temp_dep = geo_dep.merge(temp_dep, left_on = 'code', right_on = 'code_postal')
        temp_dep.drop(columns = ['code','nom'], inplace = True)
        display_df = temp_dep[temp_dep.année == a]
        code = 'code_postal'
        nom = 'departement'
        leg = 'Département'
        temp_sal = sal_dep[sal_dep.année == a]
        temp_sal = geo_dep.merge(temp_sal, left_on = 'code', right_on = 'code_postal')

    else:
        temp_reg = geo_reg.merge(temp_reg, left_on = 'code', right_on = 'code_reg')    
        temp_reg.drop(columns = ['code','nom'], inplace = True)
        display_df = temp_reg[temp_reg.année == a]
        code = 'code_reg'
        nom = 'region'
        leg = 'Région'
        temp_sal = sal_reg[sal_reg.année == a]
        temp_sal = geo_reg.merge(temp_sal, left_on = 'code', right_on = 'code_reg') 

    #La care population
    m_pop = folium.Map(location=[46.71109 ,1.7191036], zoom_start=5)

    folium.Choropleth(
        geo_data=display_df,
        name="choropleth",
        data=display_df,
        columns=[code,"population"],
        key_on="feature.properties."+code,
        threshold_scales = "population",
        fill_color="YlOrRd", 
        fill_opacity=0.7,
        line_opacity=.1,
        legend_name=leg,
    ).add_to(m_pop).geojson.add_child(
        folium.features.GeoJsonTooltip(fields = [nom, 'population'])
    )

    fig_pop = px.bar(display_df.nlargest(10,'population'), 
                y = nom, x = 'population',orientation = 'h')

    #La carte de chomeur
    m_cho = folium.Map(location=[46.71109 ,1.7191036], zoom_start=5)

    folium.Choropleth(
        geo_data=display_df,
        name="choropleth",
        data=display_df,
        columns=[code,"nombre_chomeur"],
        key_on="feature.properties."+code,
        threshold_scales = "nombre_chomeur",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=.1,
        legend_name=leg,
    ).add_to(m_cho).geojson.add_child(
        folium.features.GeoJsonTooltip(fields = [nom, 'nombre_chomeur'])
    )

    #La carte salaire
    m_sal = folium.Map(location=[46.71109 ,1.7191036], zoom_start=5)

    folium.Choropleth(
        geo_data=temp_sal,
        name="choropleth",
        data=temp_sal,
        columns=[code,"salaire_moyen"],
        key_on="feature.properties."+code,
        threshold_scales = "salaire_moyen",
        fill_color="YlGn", 
        fill_opacity=0.7,
        line_opacity=.1,
        legend_name=leg,
    ).add_to(m_sal).geojson.add_child(
        folium.features.GeoJsonTooltip(fields = [nom, 'salaire_moyen'])
    )
    
    fig_pop = px.funnel(display_df.nlargest(10,'population'), 
                y = nom, x = 'population')

    fig_cho = px.funnel(display_df.nlargest(10,'nombre_chomeur'), 
                y = nom, x = 'nombre_chomeur')

    fig_sal = px.funnel(temp_sal.nlargest(10,'salaire_moyen'), 
                y = nom, x = 'salaire_moyen')

    st.header("La population")

    #Layout des figures
    c1, c2 = st.columns((1,1))

    # call to render Folium map in Streamlit
    with c1:
        folium_static(m_pop)
    c2.subheader("Plus peuplé")
    c2.plotly_chart(fig_pop)

    b = st.sidebar.button('Backup')

    if b:
        me.backup(df,'data/indicateur_departement')

    st.header("Les chomeurs par géographie")

    #Layout des figures
    c3, c4 = st.columns((1,1))

    # call to render Folium map in Streamlit
    with c3:
        folium_static(m_cho)
    c4.subheader("Plus touché par les chomeurs")
    c4.plotly_chart(fig_cho)

    st.header("La salaire moyen")

    c5, c6 = st.columns((1,1))
    with c5:
        folium_static(m_sal)

    c6.subheader("Bien payé")
    c6.plotly_chart(fig_sal)