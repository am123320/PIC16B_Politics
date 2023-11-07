import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.politico.com/2020-election/results/alabama/house/'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # initialize empty lists to store data
    years = []
    states = []
    districts = []
    dem_votes = []
    rep_votes = []

    # find the container that holds information for each district
    district_containers = soup.find_all('div', class_='leaderboard-holder')

    for container in district_containers:
        district_name = container.find('h3').text

        # extract year, state, district information
        parts = district_name.split()

        if len(parts) >= 2:
            year = 2020
            state = parts[0][:-2] 
            district = parts[1][:-2] 
        else:
            state, district = '', ''

        table = container.find('table', class_='candidate-table')

        if table:
            rows = table.find('tbody').find_all('tr')

            for row in rows:
                candidate_name = row.find('div', class_='name-only').text
                votes = row.find('div', class_='candidate-votes-next-to-percent').text

                party_tag = row.find('div', class_='party-label').text.lower()
                if 'gop' in party_tag:
                    rep_votes.append(votes)
                elif 'dem' in party_tag:
                    dem_votes.append(votes)

                years.append(year)
                states.append(state)
            districts.append(district)

    # ensure the lists have the same length by adding dummy values for missing data
    num_rows = len(district_containers)
    while len(dem_votes) < num_rows:
        dem_votes.append('0') 
    while len(rep_votes) < num_rows:
        rep_votes.append('0')  

    data = {
        'Year': years[:num_rows],
        'State': states[:num_rows],
        'Congressional District': districts[:num_rows],
        'Dem votes': dem_votes,
        'Rep votes': rep_votes
    }

    df = pd.DataFrame(data)
    df.to_csv("politico.csv", index=False)

else:
    print('Failed to retrieve the webpage.')

