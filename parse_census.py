import numpy as np
import pandas as pd

def load_census(directory):
    census_df = pd.read_csv(directory+'/sc-est2019-agesex-civ.csv')
    census_df.drop({'SUMLEV', 'DIVISION', 'REGION'}, axis=1, inplace=True)
    # Remove 'United States'
    values = ['United States']
    census_df = census_df[census_df.NAME.isin(values) == False]
    # Restrict results to only women
    values = [0,1]
    census_df = census_df[census_df.SEX.isin(values) == False]
    # Restrict ages to 30-75, to consider the most likely cohort for breast cancer
    values = []
    for i in range(30, 76):
        values.append(i)
    census_df = census_df[census_df.AGE.isin(values) == True]
    # Group the dataframe by state, summing population totals
    grouped_census_df = census_df.groupby('STATE').apply(lambda x: x[['ESTBASE2010_CIV', 'POPEST2010_CIV', 'POPEST2011_CIV', 'POPEST2012_CIV', 'POPEST2013_CIV', 
'POPEST2014_CIV', 'POPEST2015_CIV', 'POPEST2016_CIV', 'POPEST2017_CIV', 'POPEST2018_CIV', 'POPEST2019_CIV']].sum())
    abbr = ["AL","AK","AZ","AR","CA","CO","CT","DE","DC","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]
    grouped_census_df['State Code'] = abbr
    return grouped_census_df

def join_states_tables(sites_df, census_df):
    """
    Create a joined table of sites aggregated by state, and census data aggregated by state
    Produce statistic for persons/site for the start and endpoints, and the percent change over the timeframe
    """
    joined_df = census_df.join(other=sites_df, on='State Code', how='inner')
    # 
    joined_df['2010 persons per site'] = joined_df['ESTBASE2010_CIV'] / joined_df['Count']
    joined_df['2019 persons per site'] = joined_df['POPEST2019_CIV'] / joined_df['Count']
    joined_df['Percent Change of 2010-2019 persons per site'] = 100 * (joined_df['2019 persons per site'] - joined_df['2010 persons per site'])/joined_df['2010 persons per site']
    return joined_df