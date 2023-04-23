"""
Classes:
- WeatherProcessor
"""

from datetime import date
from scrape_weather import WeatherScraper
from db_operations import DBOperations
from plot_operations import PlotOperations

class WeatherProcessor:
    """WeatherProcessor class."""
    def __init__(self):
        self.db = DBOperations('weather_data.db')
        self.scraper = WeatherScraper()
        self.plotter = PlotOperations()

    def display_menu(self):
        """Displays the main menu."""
        print("Weather Processor Menu:")
        print("1. Download weather data")
        print("2. Update weather data")
        print("3. Generate box plot for a year range")
        print("4. Generate line plot for a month and year")
        print("5. Exit")

    def run(self):
        """Runs the main loop of the program."""
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
        """Downloads the full set of weather data."""
        self.db.purge_data()
        data = self.scraper.import_weather()
        self.db.save_data(data)
        print("Weather data downloaded and saved to database.")

    def update_weather_data(self):
        """Updates the weather data with missing data between today's date and the latest date in the database."""
        latest_date = self.db.get_latest_date()
        today = date.today().strftime("%Y-%m-%d")
        if latest_date == today:
            print("Weather data is already up to date.")
            return
        data = self.scraper.scrape_and_save_missing(latest_date, today)
        self.db.save_data(data)
        print("Weather data updated and saved to database.")

    def generate_box_plot(self):
        """Generates a box plot for a year range."""
        start_year = input("Enter the start year: ")
        end_year = input("Enter the end year: ")
        data = self.db.fetch_data_for_year_range(start_year, end_year)
        if not data:
            print("No data found for the specified year range.")
            return
        self.plotter.generate_box_plot(data)

    def generate_line_plot(self):
        """Generates a line plot for a month and year."""
        year = input("Enter the year: ")
        month = input("Enter the month (1-12): ")
        data = self.db.fetch_data_for_month(year, month)
        if not data:
            print("No data found for the specified month and year.")
            return
        self.plotter.generate_line_plot(data)
