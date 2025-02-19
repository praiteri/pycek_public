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
        idx = 0
        for ds in scatter:
            if ds is not None:
                plt.scatter(ds[:,0],ds[:,1],label="Data "+str(idx)),
                idx += 1
            #     ymin = np.min(ds[:,1] - 0.1*np.abs(np.min(ds[:,1])))
            #     ymax = np.max(ds[:,1] + 0.1*np.abs(np.max(ds[:,1])))
            
            # ax = plt.gca()        
            # ax.set_ylim([ymin, ymax])

        for ds in line:
            if ds is not None:
                plt.plot(ds[:,0],ds[:,1],color='red',label="Data "+str(idx)),
                idx += 1

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
        elif output == "marimo":
            return plt.gcf()
        else:
            plt.savefig(output)
        plt.close()

