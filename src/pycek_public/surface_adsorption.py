import pycek_public as cek
import numpy as np

class surface_adsorption(cek.cek_labs):
    def setup_lab(self):
        """
        Define base information for the lab.
        They can be overwrite by the user using the kwargs in the constructor or
        by calling the set_parameters method.
        """
        self.add_metadata( 
            laboratory = 'Surface Adsorption Lab',
            columns = ["Dye added (mg)", "Dye in solution (mol/L)"]
            )
        
        self.volume = 1 # L
        self.minDye = 500 # mg
        self.maxDye = 10000 # mg
        
        self.sample_parameters = {
            "dH"       : -19.51e3, # J/mol
            "dS"       : -10, # J/mol/K
            "Q"        : 0.0001, # monolayer coverage (mol/m^2)
            "molarMass": 584.910641, # g/mol
            }

        self.number_of_values = 100 
        self.noise_level = 0.5e-5
        self.precision = 10

    def create_data(self):
        """
        Generate the data
        """
        self.set_parameters( 
            sample = self.sample,
            number_of_values = self.number_of_values,
            )

        self.add_metadata(**{
            "Temperature (C)"    : self.temperature - 273.15,
            "Volume (L)"         : self.volume,
            "Molar mass (g/mol)" : self.sample_parameters["molarMass"],
            "MinDye (mg)"        : self.minDye,
            "MaxDye (mg)"        : self.maxDye,
            'Number of values'   : self.number_of_values,
        })

        # Langmuir isotherm equilibrium constant
        # Convert to kJ/mol
        lnK = (-self.sample_parameters["dH"] / (self.temperature) + self.sample_parameters["dS"]) / self.R
        K = np.exp(lnK) # in L/mol

        conversion_factor = 1000 * self.sample_parameters["molarMass"] * self.volume
        conc_range = np.array([self.minDye, self.maxDye]) / conversion_factor

        self.data = self.generate_data_from_function(
                lambda x,K,Q: ((x*K - K*Q - 1) + np.sqrt((x*K - K*Q - 1)**2 + 4*x*K) ) / (2*K) , 
                {"K":K , "Q":self.sample_parameters["Q"]}, 
                self.number_of_values,
                xrange = conc_range, 
                xspacing = 'linear',
                noise_level = self.noise_level,
                positive = True,
                )
            
        self.data[:,0] *= conversion_factor

        return self.data

