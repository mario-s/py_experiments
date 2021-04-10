"""
Web scraping sample: get participants of Tuscany Trail in 2021
and plot a bar chart by country.
"""
import os
import json
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

URL = 'https://www.tuscanytrail.it/en/2021-edition/'

def scrap_rows():
    """
    Scrap all the rows from the table.
    """
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')

    table = soup.find('table')
    trs = table.find_all('tr')

    rows = []
    for tr in trs:
        row = [str(c.span.contents[0]) for c in tr.find_all('td')]
        rows.append(row)
    return rows

def count_frequency(a_list) -> dict:
    """
    Counts appearance of of unique items in a list and returns it as a dictionary.
    """
    freq = {}
    for key in a_list:
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

def dump_data(data, filename):
    """
    Write table data to file.
    """
    with open(filename, 'w') as file:
        file.write(json.dumps(data))
    return data

def load_data(filename):
    """
    Load table data from file.
    """
    data = []
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def get_data(filename):
    """
    Get the raw data either from local file or from web page.
    """
    if os.path.exists(filename):
        return load_data(filename)

    return dump_data(scrap_rows(), filename)

def starters_by_country():
    """
    Creates a dictionary where the key is the country and the value are the number of
    participants for that country. The dictionary is sorted by the highest value
    of participants.
    """
    tbl = get_data("tuscany_trail_starters.json")
    countries = [row[-1] for row in tbl]
    return sort_by_value(count_frequency(countries))

def plot(dic):
    """
    Create a bar plot for the participants.
    """
    _, ax = plt.subplots(figsize=(30,5))
    bars = plt.bar(dic.keys(), dic.values())

    #add values to each bar
    for bar in bars:
        height = bar.get_height()
        label_x_pos = bar.get_x() + bar.get_width() / 2
        ax.text(label_x_pos, height, s=f'{height}', ha='center', va='bottom')

    plt.title("Participants of Tuscany Trail 2021")
    plt.xlabel('Country')
    plt.ylabel('Participants')
    plt.grid(axis='y', color='0.95')

    plt.show()

participants = starters_by_country()
plot(participants)