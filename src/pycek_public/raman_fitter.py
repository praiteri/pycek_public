import numpy as np
from scipy.optimize import curve_fit
from scipy.integrate import trapezoid
import matplotlib.pyplot as plt


class RamanFitter:
    def __init__(self, wavenumbers, intensities):
        """
        Initialize the Raman fitter.
        
        Parameters:
        wavenumbers: array of Raman shift values (cm^-1)
        intensities: array of intensity values
        """
        self.wavenumbers = np.array(wavenumbers)
        self.intensities = np.array(intensities)
        self.fit_result = None
        self.fit_wavenumbers = None
        self.background_fit = None
        self.popt = None
        self.mask = None
        self.p0 = None  # Store initial guess
        
    def lorentzian(self, x, *params):
        """
        Sum of multiple Lorentzian functions.
        
        Parameters: position1, height1, width1, position2, height2, width2, ...
        (3 parameters per peak)
        """
        result = np.zeros_like(x)
        for i in range(0, len(params), 3):
            pos, height, width = params[i:i+3]
            result += height * (width**2) / ((x - pos)**2 + width**2)
        return result
    
    def lorentzian_with_background(self, x, *params):
        """
        Sum of Lorentzians plus polynomial background.
        Last 2 parameters are for linear background: a + b*x
        """
        n_peaks = (len(params) - 2) // 3
        bg_a, bg_b = params[-2:]
        background = bg_a + bg_b * x
        
        lorentz_params = params[:-2]
        result = self.lorentzian(x, *lorentz_params) + background
        return result
    
    def get_peaks_guess(self, n_peaks, freq_range=None):
        # Select data in frequency range
        if freq_range is not None:
            self.mask = (self.wavenumbers >= freq_range[0]) & (self.wavenumbers <= freq_range[1])
            x_fit = self.wavenumbers[self.mask]
            y_fit = self.intensities[self.mask]
        else:
            self.mask = np.ones(len(self.wavenumbers), dtype=bool)
            x_fit = self.wavenumbers
            y_fit = self.intensities
        p0 = self._estimate_initial_params(x_fit, y_fit, n_peaks, True)
        return p0

    def fit(self, n_peaks, freq_range=None, fix_params=None, remove_background=False, peak_positions=None):
        """
        Fit the spectrum with Lorentzian functions.
        
        Parameters:
        n_peaks: number of Lorentzian peaks to fit
        freq_range: tuple (min, max) for fitting range. If None, uses all data
        fix_params: dict with keys like 'position_0', 'height_1', 'width_2', etc.
                   Values are the fixed values for those parameters
        remove_background: if True, removes linear background before fitting
        peak_positions: list of initial peak positions. If provided, heights and widths
                       are estimated from these positions. If None, positions are auto-detected.
        
        Returns:
        popt: optimized parameters
        """
        # Select data in frequency range
        if freq_range is not None:
            self.mask = (self.wavenumbers >= freq_range[0]) & (self.wavenumbers <= freq_range[1])
            x_fit = self.wavenumbers[self.mask]
            y_fit = self.intensities[self.mask]
        else:
            self.mask = np.ones(len(self.wavenumbers), dtype=bool)
            x_fit = self.wavenumbers
            y_fit = self.intensities
        
        # Estimate initial parameters from data
        if peak_positions is not None:
            p0 = self._estimate_heights_widths(x_fit, y_fit, peak_positions, remove_background)
        else:
            p0 = self._estimate_initial_params(x_fit, y_fit, n_peaks, remove_background)
        
        self.p0 = p0  # Store initial guess
        
        # Determine which parameters to fix
        fixed_mask = self._create_fixed_mask(n_peaks, fix_params, remove_background)
        
        # Fit with constraints
        if remove_background:
            fit_func = self.lorentzian_with_background
        else:
            fit_func = self.lorentzian
        
        try:
            popt, _ = curve_fit(fit_func, x_fit, y_fit, p0=p0, maxfev=10000)
            
            # Apply fixed values
            if fixed_mask is not None:
                for i, is_fixed in enumerate(fixed_mask):
                    if is_fixed:
                        popt[i] = p0[i]
            
            self.popt = popt
            
            # Create high-resolution fit for plotting (only in fitted range)
            if freq_range is not None:
                self.fit_wavenumbers = np.linspace(freq_range[0], freq_range[1], len(x_fit) * 5)
            else:
                self.fit_wavenumbers = np.linspace(x_fit.min(), x_fit.max(), len(x_fit) * 5)
            
            self.fit_result = fit_func(self.fit_wavenumbers, *popt)
            return popt
        except RuntimeError as e:
            print(f"Fitting failed: {e}")
            return None
    
    def _estimate_initial_params(self, x, y, n_peaks, include_background):
        """Estimate initial parameters from data."""
        # Find peaks
        from scipy.signal import find_peaks
        peaks, _ = find_peaks(y, distance=len(y)//(n_peaks+1))
        
        # Use n_peaks with highest intensity
        if len(peaks) > 0:
            top_peaks = peaks[np.argsort(y[peaks])[-n_peaks:]]
        else:
            top_peaks = np.linspace(x.min(), x.max(), n_peaks)
        
        p0 = []
        for idx in sorted(top_peaks):
            p0.extend([x[idx], y[idx], 0.3])  # position, height, width
        
        if include_background:
            p0.extend([y.min(), 0.0])  # background amplitude and slope
        
        return p0

    def _estimate_heights_widths(self, x, y, peak_positions, include_background):
        """Estimate heights and widths for given peak positions."""
        p0 = []
        for pos in peak_positions:
            idx = np.argmin(np.abs(x - pos))
            height = y[idx]
            width = 0.3
            p0.extend([pos, height, width])
        
        if include_background:
            p0.extend([y.min(), 0.0])
        
        return p0
    
    def _create_fixed_mask(self, n_peaks, fix_params, include_background):
        """Create mask for fixed parameters."""
        if fix_params is None:
            return None
        
        n_params = n_peaks * 3
        if include_background:
            n_params += 2
        
        fixed_mask = [False] * n_params
        
        for param_name, value in fix_params.items():
            parts = param_name.rsplit('_', 1)
            if len(parts) == 2:
                ptype, idx = parts[0], int(parts[1])
                param_idx = int(idx) * 3
                
                if ptype == 'position':
                    fixed_mask[param_idx] = True
                elif ptype == 'height':
                    fixed_mask[param_idx + 1] = True
                elif ptype == 'width':
                    fixed_mask[param_idx + 2] = True
        
        return fixed_mask if any(fixed_mask) else None
    
    def get_peak_integrals(self):
        """
        Calculate the integral (area) under each peak using high-resolution fit data.
        
        Returns:
        list of integral values for each peak
        """
        if self.popt is None or self.fit_wavenumbers is None:
            print("No fit available. Run fit() first.")
            return None
        
        integrals = []
        n_peaks = len(self.popt) // 3 if (len(self.popt) % 3 == 0) else (len(self.popt) - 2) // 3
        
        for i in range(n_peaks):
            pos, height, width = self.popt[i*3:(i*3)+3]
            # Integral of Lorentzian: height * width * pi
            integral = height * width * np.pi
            integrals.append(integral)
        
        return integrals
    
    def get_background(self):
        """Get the background component if fitted with background removal."""
        if self.popt is None or len(self.popt) % 3 != 2:
            return None
        
        bg_a, bg_b = self.popt[-2:]
        x_vals = self.fit_wavenumbers if self.fit_wavenumbers is not None else self.wavenumbers
        return bg_a + bg_b * x_vals
    
    def plot_data(self, freq_range=None):
        """
        Plot only the input data.
        
        Parameters:
        freq_range: tuple (min, max) for plotting range. If None, plots all data
        """
        if freq_range is not None:
            mask = (self.wavenumbers >= freq_range[0]) & (self.wavenumbers <= freq_range[1])
            x_data = self.wavenumbers[mask]
            y_data = self.intensities[mask]
        else:
            x_data = self.wavenumbers
            y_data = self.intensities
        
        fig = plt.figure(figsize=(12, 6))
        plt.plot(x_data, y_data, 'o-', label='Data', alpha=0.7, linewidth=2, markersize=5)
        plt.xlabel('Raman Shift (cm$^{-1}$)')
        plt.ylabel('Intensity')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        #plt.show()
        return fig
    
    def plot_data_with_initial_guess(self, freq_range=None, n_peaks=None, peak_positions=None, remove_background=False):
        """
        Plot the input data and the initial guess for peaks.
        
        Parameters:
        freq_range: tuple (min, max) for plotting range. If None, plots all data
        n_peaks: number of peaks to estimate (required if p0 not already computed)
        peak_positions: list of initial peak positions (optional)
        remove_background: if True, includes background in initial guess
        """
        # Generate initial guess if not already available
#        if self.p0 is None:
#            if n_peaks is None:
#                print("No initial guess available. Provide n_peaks or run fit() first.")
#                return
#            
#            # Select data for estimation
#            if freq_range is not None:
#                mask = (self.wavenumbers >= freq_range[0]) & (self.wavenumbers <= freq_range[1])
#                x_fit = self.wavenumbers[mask]
#                y_fit = self.intensities[mask]
#            else:
#                x_fit = self.wavenumbers
#                y_fit = self.intensities
#            
#            # Estimate initial parameters
#            if peak_positions is not None:
#                self.p0 = self._estimate_heights_widths(x_fit, y_fit, peak_positions, remove_background)
#            else:
#                self.p0 = self._estimate_initial_params(x_fit, y_fit, n_peaks, remove_background)
        # Select data for estimation
        if freq_range is not None:
            mask = (self.wavenumbers >= freq_range[0]) & (self.wavenumbers <= freq_range[1])
            x_fit = self.wavenumbers[mask]
            y_fit = self.intensities[mask]
        else:
            x_fit = self.wavenumbers
            y_fit = self.intensities
        
        # Estimate initial parameters
        if peak_positions is None:
            if self.p0 is None:
                if n_peaks is None:
                    print("No initial guess available. Provide n_peaks or run fit() first.")
                    return
                self.p0 = self._estimate_initial_params(x_fit, y_fit, n_peaks, remove_background)
        else:
            self.p0 = self._estimate_heights_widths(x_fit, y_fit, peak_positions, remove_background)
        
        if freq_range is not None:
            mask = (self.wavenumbers >= freq_range[0]) & (self.wavenumbers <= freq_range[1])
            x_data = self.wavenumbers[mask]
            y_data = self.intensities[mask]
            fit_x = np.linspace(freq_range[0], freq_range[1], len(x_data) * 5)
        else:
            x_data = self.wavenumbers
            y_data = self.intensities
            fit_x = np.linspace(self.wavenumbers.min(), self.wavenumbers.max(), len(self.wavenumbers) * 5)
        
        # Compute initial guess (check if background is included)
        is_background = (len(self.p0) % 3 == 2)
        if is_background:
            initial_fit = self.lorentzian_with_background(fit_x, *self.p0)
        else:
            initial_fit = self.lorentzian(fit_x, *self.p0)
        
        fig = plt.figure(figsize=(12, 6))
        plt.plot(x_data, y_data, 'o-', label='Data', alpha=0.7, linewidth=2, markersize=5)
        plt.plot(fit_x, initial_fit, '-', linewidth=2, label='Initial Guess')
        plt.xlabel('Raman Shift (cm$^{-1}$)')
        plt.ylabel('Intensity')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        #plt.show()
        return fig
    
    def plot(self, show_components=True):
        """Plot the spectrum and fit in the fitted range."""
        if self.fit_result is None or self.fit_wavenumbers is None:
            print("No fit available. Run fit() first.")
            return
        
        # Get data in fitted range
        if self.mask is not None:
            x_data = self.wavenumbers[self.mask]
            y_data = self.intensities[self.mask]
        else:
            x_data = self.wavenumbers
            y_data = self.intensities
        
        fig = plt.figure(figsize=(12, 6))
        plt.plot(x_data, y_data, 'o-', label='Data', alpha=0.7)
        plt.plot(self.fit_wavenumbers, self.fit_result, '-', linewidth=2, label='Fit')
        
        if show_components and self.popt is not None:
            n_peaks = len(self.popt) // 3 if (len(self.popt) % 3 == 0) else (len(self.popt) - 2) // 3
            
            for i in range(n_peaks):
                pos, height, width = self.popt[i*3:(i*3)+3]
                peak = height * (width**2) / ((self.fit_wavenumbers - pos)**2 + width**2)
                plt.plot(self.fit_wavenumbers, peak, '--', alpha=0.5, label=f'Peak {i+1}')
            
            bg = self.get_background()
            if bg is not None:
                plt.plot(self.fit_wavenumbers, bg, ':', linewidth=2, label='Background')
        
        plt.xlabel('Raman Shift (cm$^{-1}$)')
        plt.ylabel('Intensity')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        #plt.show()
        return fig
    
    def print_results(self):
        """Print fitting results."""
        if self.popt is None:
            print("No fit available.")
            return
        
        n_peaks = len(self.popt) // 3 if (len(self.popt) % 3 == 0) else (len(self.popt) - 2) // 3
        
        print(f"\n{'='*60}")
        print(f"Fitting Results ({n_peaks} peaks)")
        print(f"{'='*60}")
        
        for i in range(n_peaks):
            pos, height, width = self.popt[i*3:(i*3)+3]
            integral = height * width * np.pi
            print(f"\nPeak {i+1}:")
            print(f"  Position:  {pos:.2f} cm⁻¹")
            print(f"  Height:    {height:.4f}")
            print(f"  Width:     {width:.4f} cm⁻¹")
            print(f"  Integral:  {integral:.4f}")
        
        if len(self.popt) % 3 == 2:
            bg_a, bg_b = self.popt[-2:]
            print(f"\nBackground (linear):")
            print(f"  Offset: {bg_a:.4f}")
            print(f"  Slope:  {bg_b:.6f}")
        
        print(f"{'='*60}\n")

    def print_results_string(self):
        """Print fitting results."""
        if self.popt is None:
            return "No fit available."

        n_peaks = len(self.popt) // 3 if (len(self.popt) % 3 == 0) else (len(self.popt) - 2) // 3

        lines = []
        lines.append("=" * 60)
        lines.append(f"Fitting Results ({n_peaks} peaks)")
        lines.append("=" * 60)

        for i in range(n_peaks):
            pos, height, width = self.popt[i*3:(i*3)+3]
            integral = height * width * np.pi
            lines.append(f"\nPeak {i+1}:")
            lines.append(f"  Position:  {pos:.2f} cm⁻¹")
            lines.append(f"  Height:    {height:.4f}")
            lines.append(f"  Width:     {width:.4f} cm⁻¹")
            lines.append(f"  Integral:  {integral:.4f}")

        if len(self.popt) % 3 == 2:
            bg_a, bg_b = self.popt[-2:]
            lines.append(f"\nBackground (linear):")
            lines.append(f"  Offset: {bg_a:.4f}")
            lines.append(f"  Slope:  {bg_b:.6f}")

        lines.append("=" * 60)

        return "\n".join(lines)

# Example usage
if __name__ == "__main__":

    # Read spectrum from file
    # Assumes a text file with two columns: wavenumber (cm-1) and intensity
    spectrum_file = "raman_spectrum.txt"
    data = np.loadtxt(spectrum_file)
    wavenumbers = data[:, 0]
    intensities = data[:, 1]
    
    # Create fitter
    fitter = RamanFitter(wavenumbers, intensities)
    
    # Data range
    data_range = (540, 555)
    # Initial peak positions
    peak_positions = [542, 546, 547]  # Your initial guesses in cm-1
    
    # Plot raw data
    fitter.plot_data(freq_range=data_range)

    # Option 1: Auto-detect peaks
    # fitter.plot_data_with_initial_guess(freq_range=data_range, n_peaks=3)
    
    # Option 2: Provide specific peak positions
    fitter.plot_data_with_initial_guess(freq_range=data_range, peak_positions=peak_positions)

    # Fit with custom peak positions
    popt = fitter.fit(
        n_peaks=3,
        freq_range=data_range,
        peak_positions=peak_positions,
        remove_background=True
    )
    
    # Print results
    fitter.print_results()
    
    fitter.plot_data_with_initial_guess(freq_range=data_range)

    # Get peak integrals
#    integrals = fitter.get_peak_integrals()
#    for i in range(len(integrals)):
#        print(f"\nIntegral of peak {i}: {integrals[i]}")
    
    # Plot final fit
    fitter.plot(show_components=True)
