import requests
from bs4 import BeautifulSoup
import pandas as pd
from dicts import abbrs
from functions import replace_if_not_number, get_url

all_data = pd.DataFrame()

years = [2014, 2016, 2020]
# figure out why 2018 is not working

state_abbrs = abbrs()
state_names = list(state_abbrs)
state_abbrs = list(state_abbrs.values())

for year in years: 
    for state in state_names:
        print(state)

        url = get_url(state, year)
        
        response = requests.get(url)
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')

        districts = []
        democratic_votes = []
        republican_votes = []
        total_votes = []

        table_check = soup.find("table", {"class": "wikitable plainrowheaders"})
        tables = soup.find_all("table", {"class": "wikitable plainrowheaders"})

        if table_check:
            for table_cd in tables:
                caption = table_cd.find("caption")
                if caption and "congressional district election" in caption.get_text().lower():
                    table = table_cd
                else:
                    table = None
                    # break

                # if table:
                print(table)
                for row in table.find_all("tr"):
                    cells = row.find_all(["th", "td"])
                    district = caption.get_text()
                    if len(cells) >= 3:
                        party = cells[1].text.strip()

                        if "Republican" in party:
                            rep_votes = replace_if_not_number(cells[3].text.strip())
                            rep_votes = int(rep_votes.replace(",", ""))
                        elif "Democratic" in party:
                            dem_votes = replace_if_not_number(cells[3].text.strip())
                            dem_votes = int(dem_votes.replace(",", ""))
                        elif any(char.isdigit() for char in party):
                            tot_votes = party
                            tot_votes = int(tot_votes.replace(",", ""))

        else:
            table_single = None
            tables_single = soup.find_all("table", {"class": "wikitable plainrowheaders"})

            for table_cd in tables_single:
                caption = table_cd.find("caption")
                if caption and "at-large" in caption.get_text().lower():
                    table_single = table_cd
                    break

            if table_single:
                district_name = 1
                for row in table_single.find_all("tr"):
                    cells = row.find_all(["th", "td"])
                    if len(cells) >= 3:
                        party = cells[1].text.strip()

                        if "Republican" in party:
                            rep_votes = replace_if_not_number(cells[3].text.strip())
                            rep_votes = int(rep_votes.replace(",", ""))
                        elif "Democratic" in party:
                            dem_votes = replace_if_not_number(cells[3].text.strip())
                            dem_votes = int(dem_votes.replace(",", ""))
                        elif any(char.isdigit() for char in party):
                            tot_votes = party
                            tot_votes = int(tot_votes.replace(",", ""))

                districts.append(district_name)
                republican_votes.append(rep_votes)
                democratic_votes.append(dem_votes)
                total_votes.append(tot_votes)

        # Create a DataFrame
        data = {
            'District': districts,
            'Democratic Votes': democratic_votes,
            'Republican Votes': republican_votes,
            'Total Votes': total_votes,
            'Year': [year] * len(districts),
            'State': state
        }

        print(data)

        df = pd.DataFrame(data)

        # Concatenate the current DataFrame to the all_data DataFrame
        all_data = pd.concat([all_data, df], ignore_index=True)

all_data['Democratic Votes'] = all_data['Democratic Votes'].astype(int)
all_data['Republican Votes'] = all_data['Republican Votes'].astype(int)
all_data['Total Votes'] = all_data['Total Votes'].astype(int)
all_data['Year'] = all_data['Year'].astype(int)

all_data.to_csv("wiki_elections.csv", index=False)