"""
Classes:
- PlotOperations
"""

import datetime
import matplotlib.pyplot as plt

class PlotOperations:
    """Plot operations for the weather"""
    def __init__(self, weather_data):
        """Initializes the plot operations."""
        self.weather_data = weather_data

    def plot_boxplot(self, temperatures, start_year, end_year):
        """Shows boxplot of mean temperatures in a date range"""
        # Clears data from previous plot
        plt.clf()

        months_range = range(1, 13)
        months_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        # Create an empty list with 12 inner lists for each month
        monthly_temperatures = [[] for _ in range(12)]

        # Populate the monthly_temperatures list with temperatures per month
        for date, mean_temp in temperatures.items():
            if mean_temp is not None:
                month = int(date.split('-')[1])  # Extract the month from the date string
                monthly_temperatures[month - 1].append(float(mean_temp))

        # Create the box plot using the monthly_temperatures data
        plt.boxplot(monthly_temperatures)

        # Set the labels for the graph
        plt.title(f'Monthly Temperature Distribution for: ({start_year}-{end_year})')
        plt.xlabel('Month')
        plt.ylabel('Temperature (°C)')
        plt.xticks(months_range, months_labels)

        # Show the plot
        plt.show()


    def plot_lineplot(self, temperatures, month, year):
        """Shows the lineplot for the specified month and year"""
        # Clears data from previous plot
        plt.clf()

        # Convert the month from string to int
        month = int(month)

        # Create a list of dates and temperatures
        dates, temps = [], []
        for day, temp in enumerate(temperatures):
            if temp is not None:
                date = datetime.date(year, month, day+1)
                dates.append(date)
                temps.append(float(temp))

        # Create the line plot using the provided data
        plt.plot(dates, temps)

        # Set the labels for the graph
        plt.title('Daily Avg Temperatures')
        plt.xlabel('Date')
        plt.ylabel('Temperature')

        # Set the y-axis ticks and tick labels
        min_temp, max_temp = min(temps), max(temps)
        tick_interval = (max_temp - min_temp) / 5
        plt.yticks([min_temp + i * tick_interval for i in range(6)], 
                [f"{min_temp + i * tick_interval:.1f}" for i in range(6)])

        # Display the plot
        plt.show()

