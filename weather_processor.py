"""
Classes:
- WeatherProcessor
"""

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import datetime
import calendar
from scrape_weather import WeatherScraper
from db_operations import DBOperations
from plot_operations import PlotOperations

class WeatherProcessor:
    """ Weather Processor class"""
    def __init__(self, master):
        self.scraper = WeatherScraper()
        self.master = master
        self.master.title("Weather Processor")

        self.start_year_var = tk.StringVar()
        self.end_year_var = tk.StringVar()
        self.month_var = tk.StringVar()
        self.year_var = tk.StringVar()

        self.weather_data = {}
        self.scraped_weather = {}
        self.dbo = DBOperations()
        self.dbo.initialize_db()
        self.plot = PlotOperations(self.weather_data)

        self.create_widgets()

    def create_widgets(self):
        """ Create the GUI widgets"""
        tk.Label(self.master, \
                 text="Welcome to my Weather Processor App by Jojo Jimena") \
                .grid(row=0, column=0, padx=10, pady=10)

        # View Weather Data Widget
        tk.Button(self.master, text="View Weather Data",
                    command=self.view_weather_data) \
                .grid(row=1, column=0, padx=10, pady=10)

        # Update Weather Data Widget
        tk.Button(self.master, text="Download/Update Weather Data",
                    command=self.download_or_update_data) \
                .grid(row=1, column=1, padx=10, pady=10)

        # Remove Weather Data Widget
        tk.Button(self.master, text="Remove Weather Data",
                    command=self.remove_weather_data) \
                .grid(row=1, column=2, padx=10, pady=10)

        # Box Plot Widgets
        tk.Label(self.master, text="Enter start year:") \
            .grid(row=2, column=0, padx=10, pady=10)
        tk.Entry(self.master, textvariable=self.start_year_var) \
            .grid(row=2, column=1, padx=10, pady=10)
        tk.Label(self.master, text="Enter end year:") \
            .grid(row=3, column=0, padx=10, pady=10)
        tk.Entry(self.master, textvariable=self.end_year_var) \
            .grid(row=3, column=1, padx=10, pady=10)
        tk.Button(self.master, text="Generate Box Plot For Year Range",
                    command=self.generate_box_plot) \
                .grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Line Plot Widgets
        tk.Label(self.master, text="Enter month:") \
            .grid(row=7, column=0, padx=10, pady=10)
        self.month_var.set("Jan")
        self.month_options = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                         "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        tk.OptionMenu(self.master, self.month_var, *self.month_options) \
            .grid(row=7, column=1, padx=10, pady=10)
        tk.Label(self.master, text="Enter year:") \
            .grid(row=8, column=0, padx=10, pady=10)
        tk.Entry(self.master, textvariable=self.year_var) \
            .grid(row=8, column=1, padx=10, pady=10)
        tk.Button(self.master, text="Generate Line Plot For Month",
                    command=self.generate_line_plot) \
                .grid(row=9, column=0, columnspan=2, padx=10, pady=10)

        # Exit Widget
        tk.Button(self.master, text="Exit",
                    command=self.master.quit) \
                .grid(row=10, column=0, columnspan=2, padx=10, pady=10)

    def view_weather_data(self):
        """Displays all current data found within the database."""
        new_window = tk.Toplevel(self.master)
        new_window.title("All Weather Data")
        new_window.geometry("750x450")

        tree = ttk.Treeview(new_window, columns=["id", "date", "location", "min_temp", \
                                                 "max_temp", "avg_temp"], show="headings")

        for col, heading in zip(tree["columns"], ["ID", "Sample Date", "Location", \
                                                  "Minimum Temperature", \
                                                  "Maximum Temperature", \
                                                  "Average Temperature"]):
            tree.column(col, width=100, minwidth=50, stretch=tk.YES, anchor=tk.CENTER)
            tree.heading(col, text=heading)

        try:
            data = self.dbo.get_all_data()
            for row in data:
                tree.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4], row[5]))

        except Exception as error:
            messagebox.showerror("Error", f"An error occurred: {error}")
            
        tree.pack(expand=1, fill=tk.BOTH)


    def download_or_update_data(self):
        """Download or update the data"""
        data = self.scraped_weather

        save = []
        for date, temp_data in data.items():
            max_temp = temp_data['Max'] if temp_data['Max'] else None
            min_temp = temp_data['Min'] if temp_data['Min'] else None
            avg_temp = temp_data['Mean'] if temp_data['Mean'] else None
            save.append((date, min_temp, max_temp, avg_temp))

        self.dbo.save_data(save)

    def remove_weather_data(self):
        """ Remove the weather data"""
        if messagebox.askokcancel("Delete Data", "Are you sure you wish to delete all the data?",
                                  icon='error'):
            self.dbo.purge_data()

    def generate_box_plot(self):
        """Generates a box plot and displays year range weather data"""
        # Clear Dictionaries
        self.scraped_weather.clear()
        self.weather_data.clear()

        start_year = self.start_year_var.get()
        end_year = self.end_year_var.get()
        try:
            start_year = int(start_year)
            end_year = int(end_year)
            if start_year <= 0 or end_year <= 0 \
                or start_year > datetime.datetime.now().year \
                or end_year > datetime.datetime.now().year \
                or start_year > end_year:
                raise ValueError()

            # Import weather data for the specified year range
            scraped_weather = self.scraper.import_weather_for_years(start_year, end_year)
            for year in range(start_year, end_year+1):
                for month in range(1, 13):
                    date = f"{year}-{month:02}-01"
                    if date in scraped_weather:
                        self.weather_data[date] = scraped_weather[date]['Mean']

            # Generate and display the box plot
            self.plot.plot_boxplot(self.weather_data, start_year, end_year)

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid year range.")

        self.scraped_weather = scraped_weather
        self.weather_data = {}
        return self.scraped_weather

    def generate_line_plot(self):
        """Generates a line plot and displays month range weather data"""
        # Clear Dictionaries
        self.scraped_weather.clear()
        self.weather_data.clear()

        get_month = self.month_var.get()
        year = int(self.year_var.get())
        month = self.month_options.index(get_month) + 1

        if year <= 0 or year > datetime.datetime.now().year:
            raise ValueError()

        # Import weather data for the specified month and year
        scraped_weather = self.scraper.import_weather_for_month(year, month)
        days_in_month = calendar.monthrange(year, month)[1]
        for date, weather_data in scraped_weather.items():
            start_date = f"{year}-{month:02d}-01"
            end_date = f"{year}-{month:02d}-{days_in_month:02d}"
            if start_date <= date <= end_date:
                self.weather_data[date] = weather_data['Mean']

        # Generate and display the line plot
        self.plot.plot_lineplot(list(self.weather_data.values()), month, year)

        self.scraped_weather = scraped_weather
        return self.scraped_weather


if __name__ == "__main__":
    root = tk.Tk()
    processor = WeatherProcessor(root)
    root.mainloop()
