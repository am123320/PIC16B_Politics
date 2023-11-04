# Using this dataset: https://www.census.gov/data/developers/data-sets/acs-5year.2014.html#list-tab-1036221584
# American Community Survey 5-Year Data (2009-2021)
# Taken heavily from https://github.com/AndrewBrodsky/election_predictions
# Want: 2014, 2016, 2018 to use as data, 2020 to predict

import numpy as np
import pandas as pd
from census import Census

api_key = "504da964b02039cd3885095fa07d63870cdae572"
census_key = Census(api_key)

years = ["2014", "2016", "2018", "2020"]

# race, sex, marital status, education, economic status

def get_info():         # returns acs codes and state abbreviations

    acs_codes = {
        "Total Population" : "B01003_001E",
        "Median Age" : "B01002_001E",
        "White" : "B02001_002E",
        "Black" : "B02001_003E",
        "American Indian" : "B02001_004E",
        "Asian" : "B02001_005E",
        "Pacific" : "B02001_006E",
        "Multiracial" : "B02001_008E",
        "Male" : "B01001_002E",
        "Female" : "B01001_026E",
        "Marital status" : "B06008_001E",
        "Not a citizen" : "B05001_006E",
        "Citizen by naturalization" : "B05001_005E",
        #"Born in state of residence" : "B05002_003E",
        #"Born in other state" : "B05002_004E",
        "Born in US" : "B05012_002E",
        "Less than HS" : "B06009_002E",
        "HS grad" : "B06009_003E",
        "Some college" : "B06009_004E",
        "Bachelor's degree" : "B06009_005E",
        "Graduate degree" : "B06009_006E",
        "Total income" : "B06010_001E",
        "No income" : "B06010_002E",
        "Median income" : "B06011_001E",
        "Total poverty" : "B06012_001E",
        "Income below poverty (White male)" : "B17001A_003E",
        "Income below poverty (White female)" : "B17001A_017E",
        "Income above poverty (White male)" : "B17001A_032E",
        "Income above poverty (White female)" : "B17001A_046E",
        "Income below poverty (Black male)" : "B17001B_003E",
        "Income below poverty (Black female)" : "B17001B_017E",
        "Income above poverty (Black male)" : "B17001B_032E",
        "Income above poverty (Black female)" : "B17001B_046E"
    }

    states = {
        "Alabama": "AL",
        "Alaska": "AK",
        "Arizona": "AZ",
        "Arkansas": "AR",
        "California": "CA",
        "Colorado": "CO",
        "Connecticut": "CT",
        "Delaware": "DE",
        "Florida": "FL",
        "Georgia": "GA",
        "Hawaii": "HI",
        "Idaho": "ID",
        "Illinois": "IL",
        "Indiana": "IN",
        "Iowa": "IA",
        "Kansas": "KS",
        "Kentucky": "KY",
        "Louisiana": "LA",
        "Maine": "ME",
        "Maryland": "MD",
        "Massachusetts": "MA",
        "Michigan": "MI",
        "Minnesota": "MN",
        "Mississippi": "MS",
        "Missouri": "MO",
        "Montana": "MT",
        "Nebraska": "NE",
        "Nevada": "NV",
        "New Hampshire": "NH",
        "New Jersey": "NJ",
        "New Mexico": "NM",
        "New York": "NY",
        "North Carolina": "NC",
        "North Dakota": "ND",
        "Ohio": "OH",
        "Oklahoma": "OK",
        "Oregon": "OR",
        "Pennsylvania": "PA",
        "Rhode Island": "RI",
        "South Carolina": "SC",
        "South Dakota": "SD",
        "Tennessee": "TN",
        "Texas": "TX",
        "Utah": "UT",
        "Vermont": "VT",
        "Virginia": "VA",
        "Washington": "WA",
        "West Virginia": "WV",
        "Wisconsin": "WI",
        "Wyoming": "WY",
        "Puerto Rico": "PY"
        }
    
    return acs_codes, states

def make_districts(acs_info, census_key):       # dataframe for all congressional district data of states
    info = []

    for keys, values in acs_info.items():
        info.append(values)

    districts = pd.DataFrame
    state_df = []
    state_FIPS = [ 1,  2,  4,  5,  6,  8,  9, 10, 12, 13, 
                  15, 16, 17, 18, 19, 20, 21, 22, 23, 24,
                  25, 26, 27, 28, 29, 30, 31, 32, 33, 34,
                  35, 36, 37, 38, 39, 40, 41, 42, 44, 45,
                  46, 47, 48, 49, 50, 51, 53, 54, 55, 56]
    
    for year in years: 
        for state in state_FIPS:
            state_df.append(Census.download("acs5", year, 
                Census.censusgeo([("state", str(state)), ("congressional district", "*",)]), info, census_key))
            
    districts = pd.concat(state_df[x] for x in range(50))

    return districts

def make_acs(districts, states):                # returns state info
    districts['INDEX1'] = districts.index.astype(str)
    districts['A'], districts['B'] = districts.INDEX1.str.split(',',1).str
    districts['STATE'], districts['C'] = districts.B.str.split(':',1).str
    districts['D'], districts['E'], districts['DISTRICT'], districts["F"] = districts.A.str.split(' ',3).str
    districts.drop(['INDEX1','A', 'B', 'C', 'D', 'E', 'F'], axis = 1, inplace = True)
    districts.reset_index(drop=True, inplace = True)

    districts.STATE = districts.STATE.str.strip()
    districts['STATE_ABBR'] = districts['STATE'].map(states)
    districts['DISTRICT'] = pd.to_numeric(districts['DISTRICT'], errors = 'coerce')

    return districts

def get_acs(census_key):
    #pd.set_option('display.expand_frame_repr', False)
    pd.set_option('display.precision', 2)
    pd.options.display.float_format = '{:,.0f}'.format

    acs_info, states = get_info()
    districts = make_districts(acs_info, census_key)
    acs = make_acs(districts, states)

    return acs

if __name__ == "__main__":
    acs = get_acs(census_key)