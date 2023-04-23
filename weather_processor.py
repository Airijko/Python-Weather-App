"""
Classes:
- WeatherProcessor
"""

"""
Part 4 – User Interaction
Tasks • Create a weather_processor.py module with a WeatherProcessor class
inside.
• When the program starts, present the user with a menu of choices.
• Allow the user to download a full set of weather data, or to update it.
◦ When updating, the program should check today’s date and the latest
date of weather available in the DB, and download what’s missing
between those two points, without duplicating any data.
• Allow the user to enter a year range of interest (from year, to year) to
generate the box plot.
• Allow the user to enter a month and a year to generate the line plot.
• Use this class to launch and manage all the other tasks.
• All user interaction should be self contained in the WeatherProcessor
class. There should be no user prompt type code anywhere else in the
program.
Input User supplies input.
Output Call the correct class methods to accomplish the tasks.

"""

from datetime import date
from scrape_weather import WeatherScraper
from db_operations import DBOperations
from plot_operations import PlotOperations

class WeatherProcessor:
    def __init__(self):
        self.db = DBOperations('weather_data.db')
        self.scraper = WeatherScraper()
        self.plotter = PlotOperations()

    def display_menu(self):
        """
        Displays the main menu.
        """
        print("Welcome to the Weather Processor!")
        print("1. Download full set of weather data")
        print("2. Update weather data")
        print("3. Generate box plot for a year range")
        print("4. Generate line plot for a month and year")
        print("5. Exit")

    def run(self):
        """
        Runs the main loop of the program.
        """
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")
            if choice == '1':
                self.download_weather_data()
            elif choice == '2':
                self.update_weather_data()
            elif choice == '3':
                self.generate_box_plot()
            elif choice == '4':
                self.generate_line_plot()
            elif choice == '5':
                print("Exiting program...")
                break
            else:
                print("Invalid choice. Please try again.")

    def download_weather_data(self):
        """
        Downloads the full set of weather data.
        """
        self.db.purge_data()
        data = self.scraper.scrape_weather()
        self.db.save_data(data)
        print("Weather data downloaded and saved to database.")

    def update_weather_data(self):
        """
        Updates the weather data with missing data between today's date and the latest date in the database.
        """
        latest_date = self.db.get_latest_date()
        today = date.today().strftime("%Y-%m-%d")
        if latest_date == today:
            print("Weather data is already up to date.")
            return
        data = self.scraper.scrape_and_save_missing(latest_date, today)
        self.db.save_data(data)
        print("Weather data updated and saved to database.")

    def generate_box_plot(self):
        """
        Generates a box plot for a year range.
        """
        start_year = input("Enter the start year: ")
        end_year = input("Enter the end year: ")
        data = self.db.fetch_data_for_year_range(start_year, end_year)
        if not data:
            print("No data found for the specified year range.")
            return
        self.plotter.generate_box_plot(data)

    def generate_line_plot(self):
        """
        Generates a line plot for a month and year.
        """
        year = input("Enter the year: ")
        month = input("Enter the month (1-12): ")
        data = self.db.fetch_data_for_month(year, month)
        if not data:
            print("No data found for the specified month and year.")
            return
        self.plotter.generate_line_plot(data)
