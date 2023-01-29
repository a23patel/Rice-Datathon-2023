import numpy as np
import pandas as pd
import addfips
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# Code taken from https://gist.github.com/JeffPaine/3083347
states = [ 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

states = {
    'AK': 'Alaska',
    'AL': 'Alabama',
    'AR': 'Arkansas',
    'AZ': 'Arizona',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DC': 'District of Columbia',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'IA': 'Iowa',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'MA': 'Massachusetts',
    'MD': 'Maryland',
    'ME': 'Maine',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MO': 'Missouri',
    'MS': 'Mississippi',
    'MT': 'Montana',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'NE': 'Nebraska',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NV': 'Nevada',
    'NY': 'New York',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VA': 'Virginia',
    'VT': 'Vermont',
    'WA': 'Washington',
    'WI': 'Wisconsin',
    'WV': 'West Virginia',
    'WY': 'Wyoming'
}

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
#    return grouped_census_df
    # Create a reverse lookup (lookup by name to find abbreviation)
    rev_states = {}
    for abb, name in states.items():
        rev_states[name] = abb
    # Now convert the FIPS codes to abbreviation
    names = census_df['NAME'].unique()
    af = addfips.AddFIPS()
    mapping = {}
    for i in range(names.shape[0]):
        code = int(af.get_state_fips(names[i]))
        mapping[code] = rev_states[names[i]]
    # Reset index to a column
    grouped_census_df['State FIPS'] = grouped_census_df.index
    # Create the state code column from the mapping
    grouped_census_df['State Code'] = grouped_census_df['State FIPS'].map(mapping)
    # Drop the old column we don't need
    grouped_census_df.drop(['State FIPS'], axis=1, inplace=True)
    return grouped_census_df

def time_series_by_state(joined_df, state):
    time_df = pd.melt(joined_df[joined_df['State Code'] == state], value_vars=['ESTBASE2010_CIV', 'POPEST2011_CIV', 'POPEST2012_CIV', 'POPEST2013_CIV', 'POPEST2014_CIV', 'POPEST2015_CIV', 'POPEST2016_CIV', 'POPEST2017_CIV', 'POPEST2018_CIV', 'POPEST2019_CIV'])
    time_df['year'] = time_df.index
    time_df['year'] = time_df['year'] + 2010
    time_df.drop(['variable'], axis=1, inplace=True)
    return time_df

def linearRegressiontrain(joined_df):
    joined_df['Predicted Population 2025'] = 0
    joined_df.reset_index(inplace = True)
    for i, state in enumerate(joined_df['State']):
        x = time_series_by_state(joined_df, state)['year'].to_numpy()
        x = x.reshape(-1,1)
        #print(x)
        y = time_series_by_state(joined_df, state)['value'].to_numpy()
        y = y.reshape(-1,1)
        #print(y)
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3)
        lm = LinearRegression()
        lm.fit(x_train, y_train)
        arr = [2025]
        year = np.array(arr).reshape(-1,1)
        evals = lm.predict(x_test)
        joined_df.at[i, 'Predicted Population 2025'] = lm.predict(year)[0]
        print(f"R^2 score for {state}: ", r2_score(y_test, evals))
        #print('R^2 Score: ', r2_score(y_test, evals))

def join_states_tables(sites_df, census_df):
    """
    Create a joined table of sites aggregated by state, and census data aggregated by state
    Produce statistic for persons/site for the start and endpoints, and the percent change over the timeframe
    """
    sites_state_vc = sites_df['State Code'].value_counts()
    sites_state_vc_df = pd.DataFrame({'State': sites_state_vc.index, 'Count':sites_state_vc})
    sites_state_vc_df
    joined_df = census_df.join(other=sites_state_vc_df, on='State Code', how='inner')
    joined_df['2010 persons per site'] = joined_df['ESTBASE2010_CIV'] / joined_df['Count']
    joined_df['2019 persons per site'] = joined_df['POPEST2019_CIV'] / joined_df['Count']
    joined_df['Percent Change of 2010-2019 persons per site'] = 100 * (joined_df['2019 persons per site'] - joined_df['2010 persons per site'])/joined_df['2010 persons per site']
    linearRegressiontrain(joined_df)
    joined_df['Percent Change of 2010-2025 persons per site'] = 100 * (joined_df['Predicted Population 2025'] - joined_df['2010 persons per site'])/joined_df['2010 persons per site']
    return joined_df