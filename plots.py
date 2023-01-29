import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
import plotly.io as pio
from urllib.request import urlopen
import json

def export_plotly_to_png(fig, filename):    # converting plotly graphs to png files
    pio.write_image(fig, filename, format='png')
    
def create_bar_plot(dataframe, x, y, color, width, height, title_name='2010 Populations per State):
    fig = px.bar(newdf, x = 'ABBR', y = 'POPEST2010_CIV', color='ABBR',  width=1000, height=650)
    fig.update_layout(
    title={
        'text': title_name,
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
    xaxis_title = "States",
    yaxis_title = "Populations",
    showlegend=False
    )
    fig.show()
    export_plotly_to_png(fig, "fig1.png")
    return fig

def pop2015_bar():
    fig = create_bar_plot(newdf, 'ABBR', 'POPEST2015_CIV', 'ABBR', 1000, 650, '2015 Populations per State')
                    

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
    export_plotly_to_png(fig, "fig4.png")
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
    export_plotly_to_png(fig, "fig5.png")
    return fig

def census_2010_map():
    fig = create_state_map(newdf, 'State', 'ESTBASE2010_CIV', cmap='Viridis')
    export_plotly_to_png(fig, "fig6.png")
    return fig
    
