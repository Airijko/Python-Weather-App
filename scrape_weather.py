"""
Classes:
- WeatherScraper: This class will be used to scrape data from the Environment Canada website
"""

from html.parser import HTMLParser
from datetime import datetime
import urllib.request
import re


class WeatherScraper:
    """This class will be used to scrape data from the Environment Canada"""

    def __init__(self):
        self.parser = self.MyHTMLParser()

    def scrape_weather(self, url):
        """Scrapes the data from the Environment Canada website and returns it as a dictionary."""
        with urllib.request.urlopen(url) as response:
            html = str(response.read())
        parser = self.MyHTMLParser()
        parser.feed(html)
        return parser.convert_weather_data()


    def import_weather(self):
        """Scrapes the data from the Environment Canada website and imports it into the database."""
        scraped_weather = {}
        month, year = datetime.now().month, datetime.now().year
        prev_weather = None

        while True:
            url = 'https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&' \
                 f'timeframe=2&StartYear=1840&EndYear=2018&Day=2&Year={year}&Month={month}'
            weather_data = self.scrape_weather(url)
            print(weather_data)

            if weather_data:
                scraped_weather.update(scraped_weather)

            if weather_data == prev_weather and weather_data:
                break

            prev_weather = weather_data
            month -= 1
            if month == 0:
                month = 12
                year -= 1

        return scraped_weather

    class MyHTMLParser(HTMLParser):
        """This class will be used to scrape data from the Environment Canada"""

        def __init__(self):
            super().__init__()
            self.table_found = False
            self.title_found = False
            self.tr_found = False
            self.td_found = False
            self.table_data = []
            self.current_temp = []
            self.daily_temps_data = []

        def handle_starttag(self, tag, attrs):
            if tag == "table":
                self.table_found = True
            if tag == "tr":
                self.tr_found = True
            if tag == "td":
                self.td_found = True
            if tag == "abbr":
                self.title_found = True
                for attr, value in attrs:
                    if attr == "title":
                        try:
                            date_str = datetime.strptime(value, '%B %d, %Y')
                            self.table_data.append(date_str.date())
                            # print(self.table_data)
                        except ValueError:
                            pass

        def handle_endtag(self, tag):
            if tag == "table":
                self.table_found = False
            if tag == "tr":
                if len(self.current_temp) == 3:
                    self.daily_temps_data.append(self.current_temp[:])
                self.current_temp.clear()
                self.tr_found = False
            if tag == "td":
                self.td_found = False
            if tag == "th":
                self.title_found = False

        def handle_data(self, data):
            """Handle data from the HTML table"""
            if self.tr_found and self.td_found:
                if re.match(r'^-?\d+(?:\.\d{1,2})?$', data) or data == 'M':
                    if len(self.current_temp) < 3:
                        self.current_temp.append(data)

        def convert_weather_data(self):
            """Convert daily_temps_data into a dictionary of dictionaries"""
            weather_data = {}
            for date, temps in zip(self.table_data, self.daily_temps_data):
                daily_temps = {'Max': None, 'Min': None, 'Mean': None}
                for i, key in enumerate(['Max', 'Min', 'Mean']):
                    try:
                        daily_temps[key] = float(temps[i])
                    except ValueError:
                        pass
                weather_data[str(date)] = daily_temps
            return weather_data

if __name__ == "__main__":
    myParser = WeatherScraper()
    myParser = WeatherScraper().import_weather()


# Testing
# parser = WeatherScraper()
# parser = parser.MyHTMLParser()
# url = 'https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&' \
#       'timeframe=2&StartYear=1840&EndYear=2018&Day=1&Year=2018&Month=5'
# response = urllib.request.urlopen(url)
# html = response.read().decode()
# parser.feed(html)
# print(parser.table_data)
# print(parser.daily_temps_data)
# daily_temps = parser.daily_temps_data
# weather_data = parser.convert_weather_data()
# print(daily_temps)
# print(weather_data)
# print(weather_data)
# print(parser.daily_temps_data)
