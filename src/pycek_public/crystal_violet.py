import pycek_public as cek
import numpy as np

class crystal_violet(cek.cek_labs):
    def setup_lab(self):
        """
        Define base information for the lab.
        They can be overwrite by the user using the kwargs in the constructor or
        by calling the set_parameters method.
        """
        self.add_metadata( 
            laboratory = 'Crystal Violet Lab',
            columns = ["Time (s)","Absorbance"]
            )

        self.expt_time = 1000
        self.number_of_values = 501
        self.noise_level = 0.05
        self.precision = 6
        self.background = 0.01
        
        self.activation_energy = 63e3 # J/mol
        self.prefactor = 5.9e9 # 1/M/s
        
        # Order wrt CV and OH
        self.alpha = 1.0
        self.beta = 0.75
        self.conc_to_abs = 160e3 # Absorbivity of CV at 590 nm (L/mol/cm)
        self.stock_solutions = {"cv" : 2.5e-5, "oh" : 0.5} # mol/L
        
        self.volumes = {"cv" : 10, "oh" : 10, "h2o" : 10.0} # mL

    def create_data(self):
        """
        Generate the data
        """
        self.set_parameters( 
            sample = self.sample,
            number_of_values = self.number_of_values,
            )

        self.add_metadata(**{
            "Temperature (C)"   : self.temperature-273.15,
            "Volume of CV (mL)" : self.volumes['cv'],
            "Volume of OH (mL)" : self.volumes['oh'],
            "Volume of H2O (mL)": self.volumes['h2o'],
        })

        vtot = np.sum( [ x + np.random.normal(0,self.noise_level,1) for x in self.volumes.values() ] )
        initial_concentration_cv = \
            self.stock_solutions["cv"] * self.volumes["cv"] / vtot

        concetration_oh = \
            self.stock_solutions["oh"] * self.volumes["oh"] / vtot

        rate_constant = self.prefactor*np.exp(-self.activation_energy/(self.R*(self.temperature)))
        pseudo_rate_constant = rate_constant * np.power(concetration_oh,self.beta)

        params = {
            "A" : initial_concentration_cv* self.conc_to_abs,
            "k" : pseudo_rate_constant    
        }

        self.data = self.generate_data_from_function(
                lambda x,A,k: A * np.exp(-k * x) , 
                params, 
                self.number_of_values,
                xrange = [0, self.expt_time], 
                xspacing = 'linear',
                noise_level = self.noise_level,
                positive = True,
                background = self.background,
                )
        
        return self.data
    
