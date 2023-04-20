"""
Python Final Project - Weather Processing App
Author: Jojo Jimena

Classes:
- WeatherScraper: A class for scraping weather data.

Functions:
- Main: The main method that runs the program.
"""

# pip install requests
# pip install beautifulsoup4

from datetime import date, timedelta
import requests
from bs4 import BeautifulSoup

# Testing how soup works
# url = ('https://climate.weather.gc.ca/climate_data/daily_data_e.html?'
#        'StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1&'
#        'Year=2018&Month=5')
# r = requests.get(url, allow_redirects=True)
# soup = BeautifulSoup(r.content, 'html.parser')
# test = soup.find('div', class_='table-responsive')
# print(test)
# print(help(soup))


class WeatherScraper:
    """
    A web scraper that extracts daily
    temperature data in Winnipeg
    """
    # Constructor
    def __init__(self, url):
        self.url = url
        self.weather_data = {}

    # Method
    def get_weather_data(self):
        """
        Get weather data method that parses the HTML content
        from the website and extracts the data
        """
        # Requests to the website
        response = requests.get(self.url)

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table that contains the weather data
        table = soup.find('div', class_='table-responsive')

        # Start from the current date to oldest available weather data
        today = date.today()
        date_str = today.strftime('%Y-%m-%d')
        daily_temps = {}

        while True:

            url = self.url.replace(date_str, '')
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find('div', class_='table-responsive')
            row = table.find_all('tr')[1]
            cols = row.find_all('td')
            max_temp = float(cols[1].text)
            min_temp = float(cols[2].text)
            mean_temp = float(cols[3].text)
            daily_temps = {'Max': max_temp, 'Min': min_temp, 'Mean': mean_temp}

            # Add the weather data to the dictionary
            self.weather_data[date_str] = daily_temps

            # Move on to the previous day
            yesterday = today - timedelta(1)
            date_str = yesterday.strftime('%Y-%m-%d')

            # Check if we have reached the end of the available weather data
            if date_str in self.weather_data:
                break

def main():
    """
    Main method that runs the program
    """
    # Define the starting URL with today's date
    today = date.today()
    url = ('http://climate.weather.gc.ca/climate_data/daily_data_e.html?'
           f'StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day={today.day}'
           f'&Year={today.year}&Month={today.month}#')


    # Create an instance of the WeatherScraper class and scrape the weather data
    scraper = WeatherScraper(url)
    scraper.get_weather_data()

    for date, temps in scraper.weather_data.items():
        print(f'Date: {date}')
        print(f'Max Temp: {temps["Max"]}')
        print(f'Min Temp: {temps["Min"]}')
        print(f'Mean Temp: {temps["Mean"]}\n')

# test
# test = WeatherScraper(url)
# test.get_weather_data()
# print(test.weather_data)