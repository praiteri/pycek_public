import time
from abc import ABC, abstractmethod
from collections import OrderedDict
from io import StringIO
from pathlib import Path
from typing import Callable, Dict, Optional, Tuple

import numpy as np
from numpy.lib.recfunctions import structured_to_unstructured

import pycek_public as cek


def set_ID(mo, lab, value):
    try:
        student_number = int(value.strip())
        if student_number <= 0:
            error = f"### Invalid Student ID: {value}"
            print(mo.md(error))
            raise ValueError(error)
        print(mo.md(f"Valid Student ID: {student_number}"))
        lab.set_student_ID(int(value))
    except ValueError:
        print(mo.md(f"### Invalid Student ID: {value}"))


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

        self.metadata = OrderedDict(
            {
                "student_ID": self.student_ID,
                "number_of_values": self.number_of_values,
                "output_file": self.output_file,
            }
        )

        self.make_plots = False
        self.logger_level = "ERROR"

        # Apply any keyword overrides before setting up the lab
        for k, w in kwargs.items():
            setattr(self, k, w)

        self.logger = cek.setup_logger(level=self.logger_level)

        # Lab-specific setup (defined by subclasses)
        self.setup_lab()

        self.list_of_data_files = []

    def __str__(self):
        return f"CHEM2000 Lab: {self.__class__.__name__}"

    # ------------------------------------------------------------------
    # Identity / configuration
    # ------------------------------------------------------------------

    def set_student_ID(self, student_ID):
        """Store the student ID in metadata. Does NOT seed the RNG."""
        if isinstance(student_ID, int):
            self.student_ID = student_ID
        elif isinstance(student_ID, str):
            student_ID = student_ID.strip()
            if student_ID.isdigit():
                self.student_ID = int(student_ID)
            else:
                raise ValueError("student_ID must be an integer")
        else:
            raise ValueError("student_ID must be an integer")
        self.update_metadata_from_attr()

    def set_token(self, token):
        self.token = token

    def _check_token(self):
        return self.token != 23745419

    def set_parameters(self, **kwargs):
        """Set one or more lab parameters by name."""
        for k, w in kwargs.items():
            if k == "student_ID":
                self.set_student_ID(w)
            else:
                setattr(self, k, w)
        self.update_metadata_from_attr()

    # ------------------------------------------------------------------
    # Metadata helpers
    # ------------------------------------------------------------------

    def add_metadata(self, **kwargs):
        for key, value in kwargs.items():
            self.metadata[key] = value

    def update_metadata_from_attr(self):
        for k in self.metadata:
            try:
                self.metadata[k] = getattr(self, k)
            except AttributeError:
                pass

    def get_metadata(self):
        return self.metadata

    # ------------------------------------------------------------------
    # Metadata I/O
    # ------------------------------------------------------------------

    def write_metadata(self, f=None):
        """Write metadata to a file (appended) or to the logger."""
        if f is None:
            def dump(s):
                self.logger.info(s)
        else:
            def dump(s):
                with open(f, "a") as file:
                    file.write(f"# {s}\n")

        for key, value in self.metadata.items():
            label = key.replace("_", " ")
            label = label[0].upper() + label[1:]
            dump(f"{label} = {value}")

    def read_metadata(self, f):
        """
        Read metadata comment lines from a data file.

        Returns
        -------
        metadata : OrderedDict
        """
        metadata = OrderedDict()
        with open(f, "r") as file:
            for line in file:
                line = line.strip()
                if not line.startswith("#"):
                    continue
                line = line.replace("#", "").strip()
                if "=" in line:
                    key, value = line.split("=", 1)
                elif ":" in line:
                    key, value = line.split(":", 1)
                else:
                    raise ValueError(f"Unknown separator in metadata line: {line!r}")
                metadata[key.strip()] = value.strip()
        return metadata

    # ------------------------------------------------------------------
    # Data file I/O
    # ------------------------------------------------------------------

    def write_data_to_file(self, **kwargs):
        """Write self.data plus metadata to a file and return the filename."""
        filename = self.output_file if self.output_file is not None else self.filename_gen.random
        self.add_metadata(output_file=filename)

        with open(filename, "w") as f:
            f.write(self.write_data_to_string(**kwargs))

        self.list_of_data_files.append(filename)
        return filename

    def write_data_to_string(self, **kwargs):
        """Serialise self.data and metadata to a CSV string."""
        columns = kwargs.get("columns") or self.metadata.get("columns")
        string = (",".join(columns) + "\n") if columns else ""

        for row in self.data:
            if isinstance(row, (list, tuple, np.ndarray)):
                string += ",".join(map(str, row)) + "\n"
            else:
                string += str(row) + "\n"

        for key, value in self.metadata.items():
            label = key.replace("_", " ")
            label = label[0].upper() + label[1:]
            string += f"# {label} = {value}\n"

        return string

    def read_data_file(self, filename=None):
        """
        Read a data file written by write_data_to_file.

        Returns
        -------
        data_array : np.ndarray
        header     : str
        metadata   : OrderedDict
        """
        if filename is None:
            raise ValueError("filename must be provided")

        comments, data_lines = [], []
        with open(filename, "r") as f:
            for line in f:
                (comments if line.startswith("#") else data_lines).append(line.strip())

        header = data_lines[0]
        csv_block = "\n".join(data_lines)

        data = np.genfromtxt(
            StringIO(csv_block),
            delimiter=",",
            comments="#",
            names=True,
            skip_header=0,
            dtype=None,
        )
        data_array = structured_to_unstructured(data)

        metadata = None
        if comments:
            metadata = OrderedDict()
            for line in comments:
                line = line.replace("#", "").strip()
                if "=" in line:
                    key, value = line.split("=", 1)
                elif ":" in line:
                    key, value = line.split(":", 1)
                else:
                    raise ValueError(f"Unknown separator in metadata line: {line!r}")
                metadata[key.strip()] = value.strip()

        if self.logger.isEnabledFor(10):  # DEBUG level
            self.logger.debug("-" * 50)
            for k, v in (metadata or {}).items():
                self.logger.debug(f"{k} = {v}")
            self.logger.debug("-" * 50)

        return data_array, header, metadata

    # ------------------------------------------------------------------
    # Data generation
    # ------------------------------------------------------------------

    def create_data_for_lab(self, sample_ID=None):
        """
        Generate a dataset for the lab.

        The RNG is seeded from the current system time (nanoseconds) so every
        call produces a unique dataset.  The seed is stored as ``sample_ID``
        in the metadata so the exact dataset can be reproduced later via
        ``reproduce_data(sample_ID)``.

        Parameters
        ----------
        sample_ID : int, optional
            Provide an explicit seed to reproduce a previously generated
            dataset.  If omitted, a fresh time-based seed is used.

        Returns
        -------
        data : object
            Whatever ``create_data`` returns for the concrete subclass.
        """
        if sample_ID is None:
            # Mask to a valid 32-bit unsigned integer for numpy
            sample_ID = time.time_ns() & 0xFFFFFFFF

        self.add_metadata(sample_ID=sample_ID)
        np.random.seed(sample_ID)
        self.logger.debug(f"RNG seeded with sample_ID = {sample_ID}")

        data = self.create_data()
        return data

    def reproduce_data(self, sample_ID):
        """
        Reproduce the exact dataset that was generated with *sample_ID*.

        Parameters
        ----------
        sample_ID : int
            The seed recorded in the data file's metadata (``Sample ID``).

        Returns
        -------
        data : object
            The same dataset that was originally produced with this seed.
        """
        sample_ID = int(sample_ID)
        self.logger.debug(f"Reproducing dataset with sample_ID = {sample_ID}")
        return self.create_data_for_lab(sample_ID=sample_ID)

    def create_data_file(self):
        """Generate data and write it to a file, returning the filename."""
        self.create_data_for_lab()
        return self.write_data_to_file()

    def get_data(self):
        return self.data

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _cleanup(self, pattern=None):
        """Delete all data files created during this session."""
        for ff in self.list_of_data_files:
            fp = Path(ff)
            if fp.exists():
                fp.unlink()
            else:
                self.logger.warning(f"File not found during cleanup: {ff}")

        if pattern is not None:
            for fp in Path(".").glob(pattern):
                fp.unlink()

    def _valid_ID(self, ID):
        return ID in ["23745411"]

    def _round_values(self, values, precision=None):
        if precision is None:
            precision = self.precision

        if isinstance(precision, float):
            precision = int(precision) if precision >= 0 else int(-np.log10(precision))
        elif not isinstance(precision, int):
            raise TypeError(f"precision must be int or float, got {type(precision)}")

        return np.round(values, decimals=precision)

    def _generate_uniform_random(self, lower, upper, n):
        return self._round_values(np.random.uniform(lower, upper, n))

    def _generate_normal_random(self, n, prm):
        arrays = []
        for p in prm:
            values = np.random.normal(p[0], p[1], size=n)
            arrays.append(self._round_values(values))

        return arrays[0] if len(arrays) == 1 else np.column_stack(arrays)

    def _generate_noise(self, n, noise_level=None, ntype="normal"):
        if noise_level is None:
            raise ValueError("noise_level must be provided")
        if noise_level <= 0:
            return np.zeros(n)
        if ntype == "normal":
            return np.random.normal(0, noise_level, size=n)
        raise ValueError(f"Unknown noise type: {ntype!r}")

    def _generate_data_from_function(self, func, params, nvalues, xrange):
        """Legacy helper — prefer generate_data_from_function for new code."""
        x = np.sort(self._generate_uniform_random(*xrange, nvalues))
        y = func(x, *params) + self._generate_noise(nvalues, self.noise_level)
        return np.column_stack((x, self._round_values(y)))

    def generate_data_from_function(
        self,
        function: Callable,
        params: Dict,
        nvalues: int,
        xrange: Optional[Tuple[float, float]] = None,
        xspacing: str = "random",
        noise_level: Optional[float] = None,
        background: Optional[float] = None,
        weights: Optional[bool] = None,
        positive: bool = False,
    ) -> np.ndarray:
        """
        Generate synthetic data from *function* with optional noise and background.

        Parameters
        ----------
        function : callable
            Model function; called as ``function(x, **params)``.
        params : dict
            Keyword arguments forwarded to *function*.
        nvalues : int
            Number of data points.
        xrange : (float, float)
            (min, max) bounds for x values.
        xspacing : {'random', 'linear'}
            How x values are spaced.
        noise_level : float, optional
            Standard deviation of Gaussian noise added to y.
        background : float, optional
            Constant offset added to all y values.
        weights : bool, optional
            Reserved — not yet implemented.
        positive : bool
            If True, replace each y with max(ε, |y|).

        Returns
        -------
        np.ndarray
            Shape (nvalues, 2) array of (x, y) pairs.
        """
        if xrange is None:
            raise ValueError("xrange must be provided as (min, max)")
        if not isinstance(nvalues, int) or nvalues <= 0:
            raise ValueError("nvalues must be a positive integer")

        if xspacing == "linear":
            x = np.linspace(*xrange, nvalues)
        elif xspacing == "random":
            x = np.sort(self._generate_uniform_random(*xrange, nvalues))
        else:
            raise ValueError(f"xspacing must be 'linear' or 'random', got {xspacing!r}")

        y = function(x, **params)

        if background is not None:
            y = y + background

        if noise_level is not None:
            y = y + self._generate_noise(nvalues, noise_level)

        if positive:
            eps = np.power(10.0, -self.precision)
            y = np.array([max(eps, abs(v)) for v in y])

        return np.column_stack((x, self._round_values(y)))

    # ------------------------------------------------------------------
    # Abstract interface
    # ------------------------------------------------------------------

    @abstractmethod
    def setup_lab(self, **kwargs):
        """Initialise lab-specific state. Called once during __init__."""

    @abstractmethod
    def create_data(self):
        """Generate and return the dataset for this lab."""
