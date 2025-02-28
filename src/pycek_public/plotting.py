import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

class plotting():

    def quick_plot(self, scatter=None, line=None, columns=["X", "Y"], output=None, hline=None):
        """
        Plot the data along with the best fit line and its associated confidence band using
        Matplotlib's object-oriented API to avoid race conditions.
    
        Parameters:
            scatter (list or array): Data to plot as scatter points
            line (list or array): Data to plot as lines
            columns (list): Axes labels (default is ["X","Y"])
            output (str): If provided, save figure to this path. If "marimo", return the figure object
            hline (float): If provided, add a horizontal line at this y-value
    
        Returns:
            None or Figure: Displays a matplotlib plot or returns the figure object if output="marimo"
    
        Example:
            >>> quick_plot(scatter=x_data, line=y_data)
        """
        # Input validation
        if scatter is None and line is None:
            raise ValueError("Either scatter or line should be provided")
    
        # Convert inputs to lists if they aren't already
        if not isinstance(scatter, list):
            scatter = [scatter] if scatter is not None else []
        if not isinstance(line, list):
            line = [line] if line is not None else []
    
        # Create figure and axes objects (OO approach)
        fig, ax = plt.subplots(figsize=(6, 6))
    
        # Plot scatter data
        idx = 0
        for ds in scatter:
            if ds is not None:
                ax.scatter(ds[:, 0], ds[:, 1], label=f"Data {idx}")
                idx += 1
    
        # Plot line data
        for ds in line:
            if ds is not None:
                ax.plot(ds[:, 0], ds[:, 1], color='red', label=f"Data {idx}")
                idx += 1
    
        # Set labels
        ax.set_xlabel(columns[0])
        ax.set_ylabel(columns[1])
    
        # Add horizontal line if specified
        if hline is not None:
            ax.axhline(hline, color='black', linestyle='--')
    
        # Add legend
        ax.legend()
    
        # Add watermark
        ax.text(0.5, 0.5, 'TEMPLATE', transform=ax.transAxes,
                fontsize=40, color='gray', alpha=0.5,
                ha='center', va='center', rotation=30)
    
        # Handle output
        if output is None:
            # Use this instead of plt.show() to avoid blocking behavior
            fig.canvas.draw_idle()
            plt.show(block=False)
        elif output == "marimo":
            return fig
        else:
            # Save the figure to the specified path
            fig.savefig(output)
    
        # Close the figure to free memory if not returning it
        if output != "marimo":
            plt.close(fig)

