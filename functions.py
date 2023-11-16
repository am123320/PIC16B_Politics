import requests
from bs4 import BeautifulSoup

def get_url(state, year):
    state_url = state.replace(" ", "_")
    multi_url = "https://en.wikipedia.org/wiki/" + str(year) + "_United_States_House_of_Representatives_elections_in_" + state_url
    one_url = "https://en.wikipedia.org/wiki/" + str(year) + "_United_States_House_of_Representatives_election_in_" + state_url

    target_text = "does not have an article"
    response = requests.get(multi_url)
    content = response.text 
    matches = find_exact_match(content, target_text)

    if matches:
        url = one_url
    else:
        url = multi_url

    return url

def find_exact_match(page_content, target_text):
    soup = BeautifulSoup(page_content, 'html.parser')
    matches = soup.find_all(string=lambda text: target_text in text)
    return bool(matches)

def replace_if_not_number(string):
    if string and not string[0].isdigit():
        string = "0"
    elif len(string) == 0: 
        string = "0"
    else:
        string = string
    return string
