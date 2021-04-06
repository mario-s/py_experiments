"""
Web scraping sample: get participants of Tuscany Trail in 2021 
and plot a bar chart by country.
"""
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
    count appearance of countries
    """
    freq = {}
    for item in countries:
        if item in freq:
            freq[item] += 1
        else:
            freq[item] = 1
    return freq

def sort_by_value(freq) -> dict:
    """
    sort the dictionary by values, this will result in a list of tuples with the highest occurence first
    """
    sorted_list = sorted(freq.items(), reverse=True, key=lambda x: x[1])
    #create a new dictionary out of the list
    return dict(sorted_list)


page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

table = soup.find('table')
rows = table.find_all('tr')

countries = find_countries(rows)
sorted_freq = sort_by_value(count_frequency(countries))

#create a bar plot
fig, ax = plt.subplots(figsize=(30,5))
bars = plt.bar(sorted_freq.keys(), sorted_freq.values())

#add values to each bar
for bar in bars:
  height = bar.get_height()
  label_x_pos = bar.get_x() + bar.get_width() / 2
  ax.text(label_x_pos, height, s=f'{height}', ha='center', va='bottom')

plt.xlabel('Country')
plt.ylabel('Participants')
plt.grid(axis='y', color='0.95')

plt.show()