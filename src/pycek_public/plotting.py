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

        ax = plt.gca()
        ax.text(0.5, 0.5, 'TEMPLATE', transform=ax.transAxes,
            fontsize=40, color='gray', alpha=0.5,
            ha='center', va='center', rotation=30)

        # Show the plot
        if output is None:
            plt.show()
        elif output == "marimo":
            return plt.gcf()
        else:
            plt.savefig(output)
        plt.close()

    ## --- END STUDENT VERSION -- ##

    def get_t_value(self, ndof, confidence=None):
        """
        Calculate the two-tailed Student's t-value for a given number of degrees of freedom
        and confidence level.

        Parameters:
            ndof (int): Number of degrees of freedom
            confidence (float): Confidence level, default is 0.95 for 95% confidence

        Returns:
            float: The critical t-value for the specified parameters

        Example:
            For 95% confidence and 10 degrees of freedom:
            >>> get_t_value(10)
            2.2281388519495335
        """
        if confidence is None:
            confidence = self._confidence_level

        # Calculate alpha (significance level) from confidence level
        # For 95% confidence, alpha = 0.05
        alpha = 1 - confidence

        # Calculate the t-value using the percent point function (PPF) of the t-distribution
        # We use alpha/2 for two-tailed test and (1 - alpha/2) for the upper tail
        tval = stats.t.ppf(1.0 - alpha/2., ndof)

        return tval

    def plot_fit_with_confidence_band(
        self, data, fit_model, popt, 
        confidence=None, output=None):
        """
        Plot the data along with the best fit line and its associated confidence band.

        Parameters:
            x_data (array-like): Independent variable data points
            y_data (array-like): Observed dependent variable values
            fit_model (callable): The model function used in the fit
            popt: Optimal parameter values from the fit
            confidence (float, optional): Confidence level for the confidence band
                                        (default is 0.95)

        Returns:
            None: Displays a matplotlib plot with data, fit line, and confidence band

        Example:
            >>> fit_result = scipy_function_fit(x_data, y_data, linear_model)
            >>> plot_fit_with_confidence_band(x_data, y_data, fit_result)
        """
        x_data = data[:,0]
        y_data = data[:,1]

        # Calculate degrees of freedom: number of data points minus number of parameters
        ndof = max(0, len(x_data) - len(popt))

        # Create the plot figure with a specified size
        plt.figure(figsize=(10, 6))

        # Plot the observed data points as a scatter plot
        plt.scatter(x_data, y_data, color='blue', label='Data')

        # Generate points for the fitted line
        # Linearly spaced between the minimum and maximum of x_data
        x_fit = np.linspace(min(x_data), max(x_data), 100)

        # Calculate the fitted y values using the optimal parameters
        y_fit = fit_model(x_fit, *popt)

        # Plot the fitted line
        plt.plot(x_fit, y_fit, 'r-', label='Best fit')

        if confidence is not None:
            # Calculate the error for the confidence band based on the data and fit
            y_err = np.sqrt(1/len(x_data) + (x_fit - np.mean(x_data))**2 /
                            np.sum((x_data - np.mean(x_data))**2))

            # t-statistic used to calculate the confidence interval
            tval = self.get_t_value(ndof, confidence)

            # Calculate the upper and lower bounds of the confidence band
            bounds = np.sqrt(np.sum((y_data - fit_model(x_data, *popt))**2) / ndof)
            y_upper = y_fit + tval * y_err * bounds
            y_lower = y_fit - tval * y_err * bounds

            # Plot the confidence band by shading the area between the upper and lower bounds
            plt.fill_between(x_fit, y_lower, y_upper,
                            color='gray', alpha=0.2,
                            label=f'{int(confidence*100)}% Confidence band')
            plt.title(f'Data with Linear Fit and {int(confidence*100)}% Confidence Bands')
        else:
            plt.title(f'Data with Linear Fit')

        # Add labels and title to the plot
        plt.xlabel('x')
        plt.ylabel('y')
    
        # ymin = np.min(y_data) - 0.1*np.abs(np.min(y_data))
        # ymax = np.max(y_data) + 0.1*np.abs(np.max(y_data))
        # ax = plt.gca()        
        # ax.set_ylim([ymin, ymax])

        # Display the legend
        plt.legend()

        # Show the plot
        if output is None:
            plt.show()
        else:
            plt.savefig(output)

    def plot_residuals(self, data, fit_model, popt):
        """
        Create a residual plot to visualize the differences between observed and predicted values.
        Residuals are the differences between actual y values and model predictions.

        Parameters:
            x_data (array-like): Independent variable data points (input for the model)
            y_data (array-like): Observed dependent variable values (true values)
            fit_model (callable): The model function used in the fit
            popt: Optimal parameter values from the fit
                The 'result' dictionary should include at least the 'popt' key, which contains the
                optimal parameters for the fitted model.

        Returns:
            None: Displays a matplotlib plot of residuals

        Example:
            >>> fit_result = scipy_function_fit(x_data, y_data, linear_model)
            >>> plot_residuals(x_data, y_data, fit_result)
        """
        x_data = data[:,0]
        y_data = data[:,1]

        # Calculate model predictions using the fitted parameters ('popt' contains optimal parameters)
        y_pred = fit_model(x_data, *popt)

        # Calculate residuals (observed y values - predicted y values)
        residuals = y_data - y_pred

        # Create a new figure with a specified size for the plot
        plt.figure(figsize=(10, 6))

        # Scatter plot of the residuals vs the x_data points
        # Each point in the scatter plot corresponds to the residual for a specific x_data value
        plt.scatter(x_data, residuals, color='blue', label='Data')

        # Add a horizontal line at y=0 for reference to see how residuals deviate from 0
        plt.axhline(y=0, color='black', linestyle='--', label='Zero Residuals')

        # Label the x and y axes
        plt.xlabel('x')  # x-axis represents the independent variable
        plt.ylabel('e')  # y-axis represents the residuals or errors (observed - predicted)

        # Add a title to the plot
        plt.title('Plot of the residuals')

        # Optionally, add a legend to clarify the plot's labels
        plt.legend()

        # Display the plot
        # plt.savefig("fit_residuals.png")
        plt.show()
