import pycek_public as cek
import numpy as np
import pprint as pp

class bomb_calorimetry(cek.cek_labs):
    def setup_lab(self):
        """
        Define base information for the lab
        """
        self.add_metadata( 
            laboratory = 'Bomb Calorimetry',
            columns = ["Time (s)","Temperature (K)"]
            )

        self.available_samples = ['benzoic', 'sucrose', 'naphthalene']

        self.ignition_time = 20
        self.relaxation_time = 3
        self.number_of_values = 100
        self.noise_level = 0.1

        self.slope_before = np.random.uniform(0., self.noise_level) / 3
        self.slope_after = np.random.uniform(0., self.noise_level) / 3
        
        self.RT = self.R * self.temperature
        
        # calorimeter constant (J/K)
        self.calorimeter_constant = {'value':10135,'std_error':0.0}
        self.sample_parameters["co2"] = {
            "mM" : 44.01,
            "dH" : -393.51e3, # co2 enthapy of formation (J/mol/K)
        }
        self.sample_parameters["h2o"] = {
            "mM" : 18.015,
            "dH" : -285.83e3,# h2o enthapy of formation (J/mol/K)
        }    
            
        self.sample_parameters["benzoic"] = {
            "mM" : 122.123,
            "n1" : 7,
            "n2" : 3,
            "dn" : 7-15/2,
            "dHf" : {'value':-384.8e3,'std_error':0.5e3},
            "dHc" : {'value':-3227.26e3,'std_error':0.2e3},
        }
        self.sample_parameters["sucrose"] = {
            "mM" : 342.3,
            "n1" : 12,
            "n2" : 11,
            "dn" : 0,
            "dHf" : {'value':-2221.2e3,'std_error':0.2e3},
            "dHc" : {'value':-5643.4e3,'std_error':1.8e3},
        }
        self.sample_parameters["naphthalene"] = {
            "mM" : 128.17,
            "n1" : 10,
            "n2" : 4,
            "dn" : 10 - 12,
            "dHf" : {'value':77e3,'std_error':10.0e3},
            "dHc" : {'value':-5160e3,'std_error':20.0e3},
        }

    def create_data(self):
        """
        Generate the data
        """
        if self.sample is None:
            raise Exception("Sample not defined")

        prm = self.sample_parameters[ self.sample ]

        self.set_parameters( 
            sample = self.sample,
            number_of_values = self.number_of_values,
            )

        self.mass = np.random.normal(1000, 100)
        self.add_metadata(**{
            'Tablet mass (mg)': self.mass,
            "Ignition time (s)" : self.ignition_time,
            "Sample" : self.sample, 
            })

        moles = self.mass / 1000 / prm["mM"]

        # combustion enthalpy
        # nH{co2} + mH{h2o} - H = DcH
        DcH = prm["n1"] * self.sample_parameters["co2"]["dH"] + \
              prm["n2"] * self.sample_parameters["h2o"]["dH"] - prm["dHf"]["value"]

        dH = DcH * moles
        dnrt = moles * self.RT * prm["dn"]
        dU = dH - dnrt
        
        deltaT = -dU / self.calorimeter_constant['value']

        x = np.linspace(0, self.number_of_values, self.number_of_values)
        y = np.random.normal(0, self.noise_level, self.number_of_values)

        dd = 0.
        T = self.temperature
        for i in range(self.number_of_values):
            if i < self.ignition_time:
                T += self.slope_before 
            else:   
                T += self.slope_after
                dd = deltaT * (1 - np.exp( - (i - self.ignition_time) / self.relaxation_time) )
            y[i] += T + dd 

        self.data = np.column_stack((x,y))

        return

