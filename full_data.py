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

first_columns = ['Year', 'State', 'State Abbr', 'District', 'Democratic Votes', 'Republican Votes', 'Total Votes',
                  'Democratic Percentage', 'Republican Percentage']
df_data = df_final[first_columns + [col for col in df_final.columns if col not in first_columns]]

#remove_penn = (df_data['Year'] == 2016) & (df_data['State'] == 'Pennsylvania') & (df_data['District'] == '19')
#df_data = df_data[~remove_penn]
df_data.to_csv('final.csv', index=False)