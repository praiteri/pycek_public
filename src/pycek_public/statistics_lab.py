import pycek_public as cek
import numpy as np

class stats_lab(cek.cek_labs):
    def setup_lab(self):
        """
        Define base information for the lab
        """
        self.add_metadata( 
                          laboratory = 'Basic Statistics Lab',
                          columns = ["X","Y"]
                          )

        self.number_of_values = 10

        self.available_samples = [
            'Averages',
            'Propagation of uncertainty',
            'Comparison of averages',
            'Linear fit',
            'Non linear fit',
            'Detection of outliers',
        ]
    
        self.sample_parameters['Averages'] = {
            "gen_values" : [
                (1.0, 0.1),
                (12., 2.0)
            ],
            'expected_value' : (1.0,10.0),
            "precision" : 3,
            }
        
        self.sample_parameters['Propagation of uncertainty'] = {
            "gen_values" : [
                (15.0, 1.0),
                (133., 2.0)
            ],
            "precision" : 3,
            }

        self.sample_parameters['Comparison of averages'] = {
            "gen_values" : [
                (15.0, 1.0),
                (13.2, 2.0)
            ],
            "precision" : 3,
            }

        self.sample_parameters['Linear fit'] = {
            "function" : lambda x,m,q: m*x + q, 
            "gen_values" : {'m':12.3 , 'q':1.0},
            "xrange" : [0.0 , 10.0],
            "expected_value" : (11.3,0.9),
            "precision" : 3,
            }

        self.sample_parameters['Non linear fit'] = {
            "nval" : 10,
            "function" : lambda x,E0,K0,Kp,V0:  E0 + K0 * x / Kp * ( (V0/x)**Kp / (Kp-1)+1) - K0*V0/(Kp-1), 
            "gen_values" : {"E0":-634.2, "K0":12.43, "Kp":4.28, "V0":99.11},
            "xrange" : [50 , 140],
            "precision" : 3,
        }
        
        self.sample_parameters['Detection of outliers'] = {
            "function" : lambda x,m,q: m*x + q, 
            "gen_values" : {'m':2.3 , 'q':0.1},
            "xrange" : [10.0 , 20.0],
            "shift" : 2,
            "precision" : 3,
            }
        
    def create_data(self):
        """
        Generate the data
        """
        if self.sample is None:
            raise Exception("Sample not defined")

        prm = self.sample_parameters[ self.sample ]
        
        self.set_parameters( 
            number_of_values = self.number_of_values,
            )
        
        if "precision" in prm:
            self.set_parameters( precision = prm["precision"] )

        if "noise" in prm:
            self.set_parameters( noise_level = prm["noise"] )

        self.add_metadata(
            number_of_values = self.number_of_values,
            sample = self.sample,
        )

        if "expected_value" in prm:
            self.add_metadata( **{"expected_value": prm["expected_value"]} )
        
        if self.sample in ["Averages", 'Propagation of uncertainty', 'Comparison of averages']:
            data = self._generate_normal_random(self.number_of_values, prm['gen_values'])

        elif self.sample in ["Linear fit"]:
            self.noise_level = 5

            data = self.generate_data_from_function(
                prm["function"], 
                prm['gen_values'], 
                self.number_of_values,
                prm['xrange'], 
                noise_level = self.noise_level,
                )

        elif self.sample in ["Non linear fit"]:
            self.noise_level = 5

            data = self.generate_data_from_function(
                prm["function"], 
                prm['gen_values'], 
                self.number_of_values,
                prm['xrange'], 
                noise_level = self.noise_level,
                )
        
        elif self.sample in ["Detection of outliers"]:
            data = self.generate_data_from_function(
                prm["function"], 
                prm['gen_values'], 
                self.number_of_values,
                prm['xrange'], 
                noise_level = self.noise_level,
                )
            i = np.random.randint(self.number_of_values)
            data[i,1] += prm['shift']

        self.data = data
        return data            

