import pandas as pd
import numpy as np

import streamlit as st

import plotly.express as px
import plotly.graph_objects as go

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def interface_predic(df,reg):

    a = st.sidebar.slider(
        label = "Année",
        min_value = 2020,
        max_value = 2035,
        step = 1
    )
    df['nombre_employe_pred'] = [reg.predict(np.array([[el]]))[0] for el in df['nombre_employe']]
    reg_pop = LinearRegression().fit(df[['année']], df['population'])
    df['population_pred'] = [reg_pop.predict(np.array([[el]]))[0] for el in df['population']]

    df_temp = pd.DataFrame({"année":[el for el in range(2020, a+1)]})
    df_temp['population_pred'] = [round(reg.predict(np.array([[el]]))[0],2) for el in df_temp['année']]
    df_temp['nombre_employe_pred'] = [round(reg_pop.predict(np.array([[el]]))[0],2) for el in df_temp['population_pred']]
 

    fig1 = px.line(df_temp, x='année', y='nombre_employe_pred') 

    fig1.update_layout(showlegend=False,
                    title_x=0.5,
                    xaxis_title='Année',
                    yaxis_title='Nombre d\'emploi',
                    width = 1400,
                    height = 400)
                         
    fig1.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))

    fig2 = px.line(df_temp, x='année', y='population_pred') 

    fig2.update_layout(showlegend=False,
                    title_x=0.5,
                    xaxis_title='Année',
                    yaxis_title='Population',
                    width = 1400,
                    height = 400)
                             
    fig2.for_each_annotation(lambda a: a.update(text=a.text.split("=")[1]))
    
    st.title("Les emplois dans les prochaines années")
    st.header("Nombre d'emplois")
    st.plotly_chart(fig1)
    st.header("La population")
    st.plotly_chart(fig2)
