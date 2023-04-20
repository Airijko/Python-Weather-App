"""
Classes:
- PlotOperations: A class for plotting weather data using Matplotlib library.
"""

# pip install matplotlib
from db_operations import DBOperations
from dbcm import DBCM
from scrape_weather import WeatherScraper
import matplotlib.pyplot as plot

class PlotOperations:
    """
    A class for plotting weather data using Matplotlib library.
    """
    def __init__(self, weather_data):
        self.weather_data = weather_data

    def plot_boxplot(self, start_year, end_year):
        """
        Plot a boxplot of the mean temperature for a given month and year.
        """
        data = []
        for month in range(1, 13):
            month_data = []
            for year in range(start_year, end_year+1):
                month_data.extend(self.weather_data[year][month])
            data.append(month_data)

        fig, ax = plot.subplots()
        ax.boxplot(data)
        ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        ax.set_title(f"Mean Temperature Boxplot ({start_year}-{end_year})")
        ax.set_xlabel("Month")
        ax.set_ylabel("Temperature (Celsius)")
        plot.show()

    def plot_lineplot(self, year, month):
        """
        Plot a lineplot of the mean temperature for a given month and year.
        """
        month_data = self.weather_data[year][month]
        fig, ax = plot.subplots()
        ax.plot(range(1, len(month_data)+1), month_data)
        ax.set_title(f"Mean Temperature Lineplot - {month}/{year}")
        ax.set_xlabel("Day")
        ax.set_ylabel("Temperature (Celsius)")
        plot.show()
