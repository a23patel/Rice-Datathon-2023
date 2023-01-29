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

def export_plotly_to_png(fig, filename):
    pio.write_image(fig, filename, format='png')

def population2010States(dataframe, state_column, var_column, cmap='Viridis'):
    fig = px.bar(newdf, x = 'ABBR', y = 'POPEST2010_CIV', color='ABBR',  width=1000, height=650)
    fig.update_layout(title={'text': "2010 Populations per State",'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'}, xaxis_title = "States", yaxis_title = "Populations", 
    showlegend=False)
    fig.show()
    return fig

def population2015States(dataframe, state_column, var_column, cmap='Viridis'):
    fig = px.bar(newdf, x = 'ABBR', y = 'POPEST2015_CIV', color='ABBR',  width=1000, height=650)
    fig.update_layout(title={'text': "2010 Populations per State",'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'}, xaxis_title = "States", yaxis_title = "Populations", 
    showlegend=False)
    fig.show()
    return fig

def population2019States(dataframe, state_column, var_column, cmap='Viridis'):
    fig = px.bar(newdf, x = 'ABBR', y = 'POPEST2019_CIV', color='ABBR',  width=1000, height=650)
    fig.update_layout(title={'text': "2019 Populations per State",'y':0.9,'x':0.5,'xanchor': 'center','yanchor': 'top'}, xaxis_title = "States", yaxis_title = "Populations", 
    showlegend=False)
    fig.show()
    return fig

def sitesperState(dataframe, county_column, var_column, cmap='Viridis'):
    sites_df = parse_sites(collab_dir+'/beginner.txt', include_PR=False)
    fig = px.histogram(sites_df, x='State Code', color='State Code', width=1000, height=650)
    fig.update_layout(title={'text': "Number of sites per State", 'y':0.9, 'x':0.5, 'xanchor': 'center','yanchor': 'top'}, xaxis_title = "States", showlegend = False)
    fig.show()
    return fig

def create_county_map(dataframe, county_column, var_column, cmap='Viridis'):
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

def census_2010_pop(dataframe, state_column, var_column, cmap='Viridis'):
    fig = px.choropleth(newdf, geojson = counties, 
                           locations='state_column',
                           locationmode="USA-states", color='var_column',
                           color_continuous_scale=cmap,
                           scope="usa",
                           labels={'State Code':'States'}
                          )

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()
    export_plotly_to_png(fig, "fig6.png")
    return fig
    
