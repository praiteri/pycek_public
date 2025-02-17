import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

class plotting():
    def quick_plot(self, scatter=None, line=None, columns=["X","Y"], output=None, hline=None):
        """
        Plot the data along with the best fit line and its associated confidence band.

        Parameters:
            data (list): List of data to plot
            columns (list): Axes labels (default is "X","Y")

        Returns:
            None: Displays a matplotlib plot with data, fit line, and confidence band

        Example:
            >>> quick_plot(x_data, y_data)
        """

        if scatter is None and line is None:
            raise ValueError("Either scatter or line should be provided")
        
        if not isinstance(scatter,list):
            scatter = [scatter]
        if not isinstance(line,list):
            line = [line]

        # Plot the observed data points as a scatter plot
        for ds in scatter:
            plt.scatter(ds[:,0],ds[:,1], color='blue', label='Data')

        # Add labels and title to the plot
        plt.xlabel(columns[0])
        plt.ylabel(columns[1])
        
        if hline is not None:
            plt.axhline(hline, color='black', linestyle='--')

        # Display the legend
        plt.legend()

        # Show the plot
        if output is None:
            plt.show()
        else:
            plt.savefig(output)
        plt.close()

