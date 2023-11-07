import censusdata
import pandas as pd

api_key = "504da964b02039cd3885095fa07d63870cdae572"

years = [2014, 2016, 2018, 2020]

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
        #"Marital status" : "B06008_001E",
        "Not a citizen" : "B05001_006E",
        #"Citizen by naturalization" : "B05001_005E",
        #"Born in state of residence" : "B05002_003E",
        #"Born in other state" : "B05002_004E",
        #"Born in US" : "B05012_002E",
        "Male 18+ birthright" : "B05003_009E",
        "Male 18+ bloodright" : "B05003_010E",
        "Male 18+ naturalized" : "B05003_011E",
        "Male 18+ not citizen" : "B05003_012E",
        "Female 18+ birthright" : "B05003_020E",
        "Female 18+ bloodright" : "B05003_021E",
        "Female 18+ naturalized" : "B05003_022E",
        "Female 18+ not citizen" : "B05003_023E",
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

    state_fips = {
        "Alabama": "01",
        "Alaska": "02",
        "Arizona": "04",
        "Arkansas": "05",
        "California": "06",
        "Colorado": "08",
        "Connecticut": "09",
        "Delaware": "10",
        "Florida": "12",
        "Georgia": "13",
        "Hawaii": "15",
        "Idaho": "16",
        "Illinois": "17",
        "Indiana": "18",
        "Iowa": "19",
        "Kansas": "20",
        "Kentucky": "21",
        "Louisiana": "22",
        "Maine": "23",
        "Maryland": "24",
        "Massachusetts": "25",
        "Michigan": "26",
        "Minnesota": "27",
        "Mississippi": "28",
        "Missouri": "29",
        "Montana": "30",
        "Nebraska": "31",
        "Nevada": "32",
        "New Hampshire": "33",
        "New Jersey": "34",
        "New Mexico": "35",
        "New York": "36",
        "North Carolina": "37",
        "North Dakota": "38",
        "Ohio": "39",
        "Oklahoma": "40",
        "Oregon": "41",
        "Pennsylvania": "42",
        "Rhode Island": "44",
        "South Carolina": "45",
        "South Dakota": "46",
        "Tennessee": "47",
        "Texas": "48",
        "Utah": "49",
        "Vermont": "50",
        "Virginia": "51",
        "Washington": "53",
        "West Virginia": "54",
        "Wisconsin": "55",
        "Wyoming": "56",
        "Puerto Rico": "72"
    }   

    state_abbrs = list(states.values())
    state_fips = list(state_fips.values())

    return acs_codes, state_abbrs, state_fips

variables, state_abbrs, state_fips = get_info()
acs_codes = list(variables.values())
acs_variables = list(variables.keys())

all_data = pd.DataFrame()

for year in years:
    for state in state_fips:
        data = censusdata.download(
            "acs5", 
            year, 
            censusdata.censusgeo([("state", state), ("congressional district", "*")]), 
            acs_codes,
            key = api_key
        )

        data["Year"] = year
        data["State FIPS"] = state
        data["State"] = state_abbrs[state_fips.index(state)]
        # data["District"] = data["congressional district"].astype(int)

        all_data = pd.concat([all_data, data])

all_data.reset_index(inplace=True, drop=True)
#all_data["District"] = all_data["congressional district"]

inv_map = {v: k for k, v in variables.items()}
all_data.rename(columns=inv_map, inplace=True)

all_data.to_csv("census.csv", index=False)
all_data.to_json("census.json", orient="records")