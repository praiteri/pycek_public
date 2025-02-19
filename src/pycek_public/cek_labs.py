import pycek_public as cek
import numpy as np
from collections import OrderedDict

from abc import ABC, abstractmethod
class cek_labs(ABC):
    def __init__(self, **kwargs):        
        self.token = None
        self.student_ID = 123456789

        self.noise_level = 1
        self.precision = 1
        
        self.available_samples = []
        self.sample_parameters = {}
        self.sample = None

        self.R = 8.314
        self.NA = 6.022e23
        self.temperature = 298

        self.number_of_values = 10
        self.output_file = None
        self.filename_gen = cek.TempFilenameGenerator()

        self.metadata = OrderedDict({
            'student_ID' : self.student_ID,
            'number_of_values' : self.number_of_values,
            'output_file' : self.output_file,
        })
        
        self.make_plots = False
        self.logger_level = "ERROR"

        # Define some lab specific parameters
        # Can overwrite the defaults
        for k,w in kwargs.items():
            setattr(self, k, w)
        np.random.seed(self.student_ID)

        self.logger = cek.setup_logger(level=self.logger_level)
        # self.logger.debug("This is a debug message")
        # self.logger.verbose("This is a verbose message")  # New verbose level
        # self.logger.info("This is an info message")
        # self.logger.result("This is an result message")
        # self.logger.warning("This is a warning message")
        # self.logger.error("This is an error message")
        # self.logger.critical("This is a critical message")
        # quit()

        # Lab specific parameters
        self.setup_lab()

        self.list_of_data_files = []

    def __str__(self):
        return f'CHEM2000 Lab: {self.__class__.__name__}'

    def set_student_ID(self,student_ID):
        if isinstance(student_ID,int):
            self.student_ID = student_ID
        elif isinstance(student_ID,str):
            student_ID = student_ID.strip()
            if student_ID.isdigit():
                self.student_ID = int(student_ID)
            else:
                raise ValueError("student_ID must be an integer")
        else:
            raise ValueError("student_ID must be an integer")
        np.random.seed(self.student_ID)
        self.update_metadata_from_attr()
        self.logger.critical(f"Initial seed = {np.random.get_state()[1][0]}")

    def set_token(self, token):
        self.token = token
        #print(f"Check: {self._check_token()}")

    def _check_token(self):
        if self.token != 23745419:
            return True
        return False

    def add_metadata(self, **kwargs):
        for key, value in kwargs.items():
            self.metadata[key] = value
        return
    
    def update_metadata_from_attr(self):
        for k in self.metadata:
            try:
                self.metadata[k] = getattr(self, k)
            except:
                pass
        return
    
    def set_parameters(self, **kwargs):
        """
        Set parameters for the lab
        """
        for k,w in kwargs.items():
            if k == "student_ID":
                self.set_student_ID(w)
            else:
                setattr(self, k, w)
        self.update_metadata_from_attr()
        return

    def write_metadata(self,f=None):
        """
        Write metadata to the data file
        """
        if f is None:
            def dump(s):
                self.logger.info(s)
        else:
            def dump(s):
                with open(f, 'a') as file:
                    file.write(f"# {s}\n")

        for key, value in self.metadata.items():
            string = f"{key}"
            string = string.replace("_"," ")
            string = string[0].upper() + string[1:] + f" = {value}"
            dump(string)

    def read_metadata(self,f):
        """
        Read metadata from the data file
        
        Return: metadata (dict)
        """
        metadata = OrderedDict({})

        hash_lines = []
        with open(f, 'r') as file:
            for line in file:
                if line.strip().startswith('#'):
                    hash_lines.append(line.replace('#','').strip())
        
        for l in hash_lines:
            if ":" in l:
                key, value = l.split(':')
            elif "=" in l:
                key, value = l.split('=')
            else:
                raise Exception("Unknown separator")
            key = key.replace("#","").strip()
            metadata[key] = value.strip()
            
        return metadata

    def write_data_to_file(self, **kwargs):
        """
        """
        if self.output_file is None:
            filename = self.filename_gen.random
        else:
            filename = self.output_file
        self.add_metadata(output_file=filename)

        with open(filename, 'w') as f:
            # Write the column names
            cols = None
            if "columns" in kwargs:
                cols = kwargs["columns"]
            elif "columns" in self.metadata:
                cols = self.metadata["columns" ]
            if cols is not None:
                f.write(",".join(cols) + "\n")

            # Convert NumPy array to list if needed
            # if isinstance(self.data, np.ndarray):
            #     self.data = self.data.tolist()

            # Write data
            for row in self.data:
                # Handle multiple columns
                if isinstance(row, (list, tuple, np.ndarray)):
                    line = ",".join(map(str, row))
                # Handle single-column case
                else:
                    line = str(row)
                f.write(line + "\n")

        # Write the kwargs as metadata
        self.write_metadata(filename)

        self.list_of_data_files.append( filename )

        return filename

    def read_data_file(self,filename=None):
        if filename is None:
            raise ValueError("Filename is missing")

        # Read file and separate comments from data
        comments = []
        data_lines = []

        with open(filename, "r") as f:
            for line in f:
                if line.startswith("#"):
                    comments.append(line.strip())  # Store comment lines
                else:
                    data_lines.append(line.strip())  # Store data lines

        # Extract header and data
        header = data_lines[0]  # First non-comment line is the header
        data_lines = "\n".join(data_lines[0:])  # Join remaining lines as CSV data

        # Convert CSV data to NumPy array
        from io import StringIO
        from numpy.lib.recfunctions import structured_to_unstructured

        data = np.genfromtxt(
            StringIO(data_lines), delimiter=',', 
            comments='#', names=True, 
            skip_header=0, dtype=None)   
        
        data_array = structured_to_unstructured(data)

        metadata = None
        if len(comments) > 0:
            metadata = OrderedDict({})
            for l in comments:
                if ":" in l:
                    key, value = l.split(':')
                elif "=" in l:
                    key, value = l.split('=')
                else:
                    raise Exception("Unknown separator")
                key = key.replace("#","").strip()
                metadata[key.strip()] = value.strip()

        self.logger.debug("-"*50)
        for k,v in metadata.items():
            self.logger.debug(f"{k} = {v}")
        self.logger.debug("-"*50)
        # Output results
        # print("Comments:")
        # print("\n".join(comments))
        # print("\nExtracted Data:")
        # print(data_array)
        return data_array, header, metadata
    
    def _cleanup(self, pattern=None):
        from pathlib import Path
        for ff in self.list_of_data_files:
            # Check if file exists before deleting
            file_path = Path(ff)
            if file_path.exists():
                file_path.unlink()
            else:
                print("The file does not exist")

        # Delete multiple files using a pattern
        if pattern is not None:
            for file_path in Path('.').glob(pattern):
                file_path.unlink()

    # def process_file(self, filename=None):
    #     self.read_data(filename)
    #     result = self.process_data()
    #     return result
    
    def _valid_ID(self,ID):
        if ID in ["23745411"]:
            return True
        return False
        
    def _round_values(self, values, precision=None):
        if precision is None:
            precision = self.precision
        rounded_values = [round(v, precision) for v in values]
        values = np.array(rounded_values, dtype=float)
        return values
    
    def _generate_uniform_random(self, lower, upper, n):
        return self._round_values(np.random.uniform(lower, upper, n))

    def _generate_normal_random(self,n,prm):
        list_of_1d_arrays = []
        for p in prm:
            values = np.random.normal(p[0], p[1], size=n)
            list_of_1d_arrays.append(self._round_values(values))

        if len(prm) == 1:
            return np.array(self._round_values(values))
        else:
            return np.column_stack( [*list_of_1d_arrays] )

    def _generate_noise(self,n,noise_level=None,ntype="normal"):
        if noise_level == None:
            raise ValueError("Missing noise level")
        if noise_level <= 0:
            return np.zeros(n)
        if ntype == "normal":
            return np.random.normal(0, noise_level, size=n)

    def _generate_data_from_function(self, func, params, nvalues, xrange):
        x = np.sort(self._generate_uniform_random(nvalues,*xrange))
        y = func(x, *params) + self._generate_noise(nvalues)
        y = self._round_values(y)
        return np.column_stack((x,y))

    import numpy as np
    from typing import Callable, Dict, Optional, Union, Tuple

    def generate_data_from_function(
        self,
        function: Callable,
        params: Dict,
        nvalues: int,
        xrange: Optional[Tuple[float, float]] = None,
        xspacing: str = 'random',
        noise_level: Optional[float] = None,
        background: Optional[float] = None,
        weights: Optional[bool] = None,
        positive: bool = False
    ) -> np.ndarray:
        """
        Generate synthetic data points from a given function with optional noise and background.

        Parameters
        ----------
        function : callable
            The model function to generate data from. Should accept x values and **kwargs.
        params : dict
            Parameters to pass to the function as keyword arguments.
        nvalues : int
            Number of data points to generate.
        xrange : tuple of float, optional
            Range of x values (min, max). Required if generating data points.
        xspacing : str, default='random'
            Method to space x values. Options:
            - 'linear': Evenly spaced points
            - 'random': Uniformly distributed random points
        noise_level : float, optional
            Standard deviation of Gaussian noise to add to y values.
        background : float, optional
            Constant background level to add to all y values.
        weights : bool, optional
            If True, include weights in output (NOT IMPLEMENTED).
        positive : bool, default=False
            If True, take absolute value of final y values.

        Returns
        -------
        np.ndarray
            2D array with shape (nvalues, 2) containing (x, y) pairs.

        Raises
        ------
        ValueError
            If xrange is None or invalid xspacing type is provided.
        """
        # Validate inputs
        if xrange is None:
            raise ValueError("xrange must be provided as (min, max) tuple")
        
        if not isinstance(nvalues, int) or nvalues <= 0:
            raise ValueError("nvalues must be a positive integer")

        # Generate x values
        if xspacing == "linear":
            x = np.linspace(*xrange, nvalues)
        elif xspacing == "random":
            x = np.sort(self._generate_uniform_random(*xrange, nvalues))
        else:
            raise ValueError(f"xspacing must be 'linear' or 'random', got '{xspacing}'")

        # Generate base y values from function
        y = function(x, **params)

        # Add optional modifications
        if background is not None:
            y += background
        
        if noise_level is not None:
            y += self._generate_noise(nvalues,noise_level)
        
        if positive:
            eps = np.power(10.,-self.precision)
            y = [ max(eps,np.abs(x)) for x in y ]

        # Note: weights parameter is currently unused
        if weights is not None:
            # TODO: Implement weights handling
            pass

        y = self._round_values(y)

        return np.column_stack((x, y))

    def create_data_file(self):
        data = self.create_data()
        self.write_data_to_file(
            self.metadata['output_file'], 
            data, **self.metadata )
        return self.metadata['output_file']
    
    def get_data(self):
        return self.data
    def get_metadata(self):
        return self.metadata

    @abstractmethod
    def setup_lab(self,**kwargs):
        pass

    @abstractmethod
    def create_data(self):
        pass

