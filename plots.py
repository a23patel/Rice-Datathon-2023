import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from urllib.request import urlopen
import json

def export_plotly_to_png(fig, filename):    # converting plotly graphs to png files
    pio.write_image(fig, filename, format='png')

def population2010States(newdf):
    fig = px.bar(newdf, x = 'ABBR', y = 'POPEST2010_CIV', color='ABBR',  width=1000, height=650)
    fig.update_layout(title={'text': "2010 Populations per State",'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'}, xaxis_title = "States", yaxis_title = "Populations", 
    showlegend=False)
    export_plotly_to_png(fig, 'fig1.png')
    return fig

def population2015States(newdf):
    fig = px.bar(newdf, x = 'ABBR', y = 'POPEST2015_CIV', color='ABBR',  width=1000, height=650)
    fig.update_layout(title={'text': "2010 Populations per State",'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'}, xaxis_title = "States", yaxis_title = "Populations", 
    showlegend=False)
    export_plotly_to_png(fig, 'fig2.png')
    return fig

def population2019States(newdf):
    fig = px.bar(newdf, x = 'ABBR', y = 'POPEST2019_CIV', color='ABBR',  width=1000, height=650)
    fig.update_layout(title={'text': "2019 Populations per State",'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'}, xaxis_title = "States", yaxis_title = "Populations", 
    showlegend=False)
    export_plotly_to_png(fig, 'fig3.png')
    return fig

def sitesperState(sites_df):
    fig = px.histogram(sites_df, x='State Code', color='State Code', width=1000, height=650)
    fig.update_layout(title={'text': "Number of sites per State", 'y':0.9, 'x':0.5, 'xanchor': 'center','yanchor': 'top'}, xaxis_title = "States", showlegend = False)
    export_plotly_to_png(fig, 'fig4.png')
    return fig

def create_county_map(dataframe, county_column, var_column, cmap='Viridis', filename='fig5.png'):
    counties = None
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)

    sites_county_vc = dataframe[county_column].value_counts()
    sites_county_vc_df = pd.DataFrame({'County': sites_county_vc.index, 'Count':sites_county_vc})

    fig = px.choropleth(sites_county_vc_df, geojson = counties, locations='County', color='Count',
                           color_continuous_scale=cmap,
                           scope="usa",
                           labels={'State Code':'States'}
                          )

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    export_plotly_to_png(fig, filename)
    return fig

def create_state_map(dataframe, state_column, var_column, cmap='Viridis', filename='fig6.png'):
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
    export_plotly_to_png(fig, filename)
    return fig

def census_2010_map(dataframe, state_column, var_column, cmap='Viridis', filename='fig7.png'):
    fig = create_state_map(dataframe, 'State', 'ESTBASE2010_CIV', cmap='Viridis', filename=filename)
    export_plotly_to_png(fig, filename)
    return fig
 
def pop_change_2010_2019(dataframe, state_column, var_column, cmap='Viridis', filename='fig8.png'):
    fig = create_state_map(dataframe, 'State', 'Percent Change 2010-2019', cmap='Viridis', filename=filename)
    export_plotly_to_png(fig, filename)
    return fig

def plot_2019_pop_per_site(dataframe, state_column, var_column, cmap='Viridis', filename='fig9.png'):
    fig = create_state_map(dataframe, 'State', '2019 persons per site', cmap='Viridis', filename=filename)
    export_plotly_to_png(fig, filename)
    return fig
                      
def plot_2010_2019_per_site_change(dataframe, state_column, var_column, cmap='Viridis', filename='fig10.png'):
    fig = create_state_map(dataframe, 'State', 'Percent Change of 2010-2019 persons per site', cmap='Viridis', filename=filename)
    export_plotly_to_png(fig, filename)
    return fig

def plot_2010_2025_per_site_change(dataframe, state_column, var_column, cmap='Viridis', filename='fig11.png'):
    fig = create_state_map(dataframe, 'State', 'Percent Change of 2010-2025 persons per site', cmap='Viridis', filename=filename)
    export_plotly_to_png(fig, filename)
    return fig
