"""
Web scraping sample: get participants of Tuscany Trail in 2021 
and plot a bar chart by country.
"""
import os
import _pickle as pickle
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

URL = 'https://www.tuscanytrail.it/en/2021-edition/'

def find_countries(rows) -> list:
    """
    grap all countries from the website
    """
    countries = []
    for row in rows:
        cols = row.find_all('td')
        #last column contains the country
        country_col = cols[-1]
        countries.append(country_col.span.contents[0])
    return countries

def count_frequency(countries) -> dict:
    """
    Count appearance of countries
    """
    freq = {}
    for item in countries:
        key = str(item)
        if key in freq:
            freq[key] += 1
        else:
            freq[key] = 1
    return freq

def sort_by_value(freq) -> dict:
    """
    sort the dictionary by values, this will result in a list of tuples with the highest occurence first
    """
    sorted_list = sorted(freq.items(), reverse=True, key=lambda x: x[1])
    #create a new dictionary out of the list
    return dict(sorted_list)

def scrap_participants():
    """
    Scrap participants from the website.
    """
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    table = soup.find('table')
    rows = table.find_all('tr')

    countries = find_countries(rows)
    return sort_by_value(count_frequency(countries))

def dump_dict(dic, filename):
    """
    Write dictionary to file.
    """
    file = open(filename, "wb")
    pickle.dump(dic, file)

def load_dict(filename):
    """
    Load dictionary from file.
    """
    file = open(filename, "rb")
    return pickle.load(file)

def get_participants():
    filename = "participants.pkl"
    #if we have a local file, load it
    if os.path.exists(filename):
        return load_dict(filename)
        
    #if participants dump is not present scrap it from the page
    participants = scrap_participants()
    #write result to file
    dump_dict(participants, filename)
    return participants

def plot(dict):
    #create a bar plot
    _, ax = plt.subplots(figsize=(30,5))
    bars = plt.bar(participants.keys(), participants.values())

    #add values to each bar
    for bar in bars:
        height = bar.get_height()
        label_x_pos = bar.get_x() + bar.get_width() / 2
        ax.text(label_x_pos, height, s=f'{height}', ha='center', va='bottom')

    plt.xlabel('Country')
    plt.ylabel('Participants')
    plt.grid(axis='y', color='0.95')

    plt.show()

participants = get_participants()
plot(participants)