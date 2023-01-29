import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns

from urllib.request import urlopen
import json

def create_county_map(dataframe, county_column, var_column, cmap='Viridis'):
    counties = None
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)

    fig = px.choropleth(dataframe, geojson = counties, locations=county_column, color=var_column,
                           color_continuous_scale=cmap,
                           scope="usa",
                           labels={'State Code':'States'}
                          )

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

def create_state_map(dataframe, state_column, var_column, cmap='Viridis'):
    counties = None
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)

    fig = px.choropleth(dataframe, geojson = counties, 
                           locations=state_column,
                           locationmode="USA-states", color=var_column,
                           color_continuous_scale=cmap,
                           scope="usa",
                           labels={'State Code':'States'}
                          )

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig
