"""
Classes:
- PlotOperations
"""
import matplotlib.pyplot as plt

class PlotOperations:
    """Plot operations for the weather"""
    def __init__(self, weather_data):
        """Initializes the plot operations."""
        self.weather_data = weather_data

    def plot_mean_temps_boxplot(self, start_year, end_year):
        """Plots a boxplot of the mean temperatures for a given range of years."""
        data = []
        for month in range(1, 13):
            month_temps = []
            for year in range(start_year, end_year + 1):
                if year in self.weather_data and month in self.weather_data[year]:
                    month_temps.extend(self.weather_data[year][month])
            data.append(month_temps)
        fig, ax = plt.subplots()
        ax.boxplot(data)
        ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        ax.set_ylabel('Temperature (°C)')
        ax.set_title(f'Mean Temperatures {start_year}-{end_year}')
        plt.show()

    def plot_mean_temps_lineplot(self, year, month):
        """Plots a lineplot of the mean temperatures for a given year and month."""
        if year not in self.weather_data or month not in self.weather_data[year]:
            print(f'No data available for {year}-{month}')
            return
        data = self.weather_data[year][month]
        fig, ax = plt.subplots()
        ax.plot(range(1, len(data)+1), data)
        ax.set_xlabel('Day')
        ax.set_ylabel('Temperature (°C)')
        ax.set_title(f'Mean Temperatures for {year}-{month}')
        plt.show()