import pandas as pd
from dicts import abbrs

abbrs_data = abbrs()
df_abbr = pd.DataFrame(list(abbrs_data.items()), columns=['State', 'State Abbr'])

df_votes = pd.read_csv('wiki_elections.csv')
df_votes = pd.merge(df_votes, df_abbr[['State', 'State Abbr']], on='State', how='left')

df_census = pd.read_csv('census.csv')
df_votes['District'] = df_votes['District'].astype(str)
df_census['District'] = df_census['District'].astype(str)
merge_columns = ['Year', 'State Abbr', 'District']
df_final = pd.merge(df_votes, df_census, on=merge_columns, how='left')

df_final['Democratic Percentage'] = (df_final['Democratic Votes'] / df_final['Total Votes']) * 100
df_final['Republican Percentage'] = (df_final['Republican Votes'] / df_final['Total Votes']) * 100
df_final['Democratic Percentage'] = df_final['Democratic Percentage'].round(2)
df_final['Republican Percentage'] = df_final['Republican Percentage'].round(2)

df_final['Voting Eligible Male'] = df_final["Male 18+ birthright"] + df_final["Male 18+ bloodright"] + df_final["Male 18+ naturalized"]
df_final['Voting Eligible Female'] = df_final["Female 18+ birthright"] + df_final["Female 18+ bloodright"] + df_final["Female 18+ naturalized"]
df_final['Voting Eligible Population'] = df_final['Voting Eligible Male'] + df_final['Voting Eligible Female']
df_final['Voter Turnout'] = (df_final['Total Votes'] / df_final['Voting Eligible Population']) * 100
df_final['Voter Turnout'] = df_final['Voter Turnout'].round(2)

first_columns = ['Year', 'State', 'State Abbr', 'District', 'Democratic Votes', 'Republican Votes', 'Total Votes',
                  'Democratic Percentage', 'Republican Percentage', 'Voting Eligible Male', 'Voting Eligible Female', 
                  'Voting Eligible Population', 'Total Population', 'Voter Turnout']
df_data = df_final[first_columns + [col for col in df_final.columns if col not in first_columns]]

keep_as_float = ['Democratic Percentage', 'Republican Percentage', 
                 'Voter Turnout', 'Year', 'State', 'State Abbr', 
                 'District', 'Median Age']
change_to_int = [col for col in df_data.columns if col not in keep_as_float]
df_data[change_to_int] = df_data[change_to_int].fillna(0).astype(int)
df_data[change_to_int] = df_data[change_to_int].astype(int)


remove_pa19 = (df_data['Year'] == 2016) & (df_data['State'] == 'Pennsylvania') & (df_data['District'] == '19')
remove_ca44 = (df_data['Year'] == 2020) & (df_data['State'] == 'California') & (df_data['District'] == '44')
df_data = df_data[~remove_pa19]
df_data = df_data[~remove_ca44]

df_data.to_csv('final.csv', index=False)