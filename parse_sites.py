import numpy as np
import pandas as pd
import zipcodes
import addfips

def replace_zipcodes(zips, af_obj):
    """
    Fetch a FIPS county code for the given ZIP code, if possible, otherwise return None

    We pass an AddFIPS object in here so that only one such object need be instantiated
    """
    try:
        zip_info = zipcodes.matching(zips)[0]
    except:
        print(f"Unable to parse zip code {zips}")
        return None
    # We need the state, and the county name (minus the "County" or "Parish" part), for addfips to look it up correctly
    county_name = "".join(zip_info['county'].split(' ')[:-1])
    state_name = zip_info['state']
    return af_obj.get_county_fips(county_name, state=state_name)

def parse_sites(site_file, include_PR=True):
    """
    Process the beginner.txt file for the relevant location information needed for the choropleth maps

    The resulting Pandas DataFrame contains a subsequence of the site name, plus the location information
    """
    fips = []
    states = []
    cities = []
    names = []
    with open(site_file, 'r') as f:
        # Discard the initial line
        _ = f.readline()
        # Parse remaining lines from the end, since name/address fields contain spurious commas
        line_no = 2e6
        i = 0
        print(f"Beginning parsing file {site_file}...")
        af = addfips.AddFIPS()
        for line in f.readlines():
            i += 1
            if i % 1000 == 0:
                print(f"Parsed {i} records.")
            if i == line_no:
                break
            try_parse = line.split(',')
            # We only want the ZIP part of the ZIP+4
            zip_part = try_parse[-3].split('-')[0]
            state_code = try_parse[-4]
            if not include_PR and state_code == 'PR':
                continue
            city = try_parse[-5]
            excess = try_parse[:-5]
            # If it's a ZIP+4 but without a hyphen, we take just the first 5
            if len(zip_part) == 9:
                zip_part = zip_part[:5]
            # TODO Now we're going to ignore rows in military bases and overseas territories
            #fips.append(int(zip_part))
            fips_code = replace_zipcodes(zip_part, af)
            if fips_code:
                fips.append(fips_code)
                states.append(state_code)
                cities.append(city)
                names.append("".join(excess)[:20])
            
    return pd.DataFrame({"Namestring": names, 
                         "FIPS County Code": fips, 
                         "State Code": states, 
                         "City": cities})

def aggregate_by_state(sites_df):
    sites_state_vc = sites_df['State Code'].value_counts()
    sites_state_vc_df = pd.DataFrame({'State': sites_state_vc.index, 'Count':sites_state_vc})
    return sites_state_vc_df

def aggregate_by_county(sites_df):
    sites_county_vc = sites_df['FIPS County Code'].value_counts()
    sites_county_vc_df = pd.DataFrame({'County': sites_county_vc.index, 'Count':sites_county_vc})
    return sites_county_vc_df