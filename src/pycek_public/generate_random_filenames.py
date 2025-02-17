import os
from glob import glob
import secrets
import string

class TempFilenameGenerator:
    """
    Generates temporary filenames with .pdb extension and increasing indices.
    Supports both sequential (tmp.{index}.pdb) and random (tmp.{random}.pdb) formats.
    """
    def __init__(self, directory=".", root="data", ext="csv", random_length=12):
        """
        Initialize the generator with a target directory.
        
        Args:
            directory (str): Directory for the filenames (default: current directory)
            root (str): Root name for the temporary files (default: tmp)
            ext (str): File extension (default: pdb)
            random_length (int): Length of random string in random filenames (default: 12)

        Example:
            generator = TempFilenameGenerator()

            # Get sequential filename (e.g., "tmp.0.pdb")
            sequential_file = generator.next

            # Get random filename (e.g., "tmp.j4k3h2l5m9n8.pdb")
            random_file = generator.random
        """
        self.directory = directory
        self.root = root
        self.ext = ext
        self.random_length = random_length
        self._current_index = self._find_max_index()
        self._current_filename = None

    def _find_max_index(self):
        """Find the highest existing index in the directory."""
        pattern = os.path.join(self.directory, f"{self.root}.*.{self.ext}")
        existing_files = glob(pattern)
        
        if not existing_files:
            return -1
            
        indices = []
        for filename in existing_files:
            try:
                # Extract index from tmp.{index}.pdb
                index = int(os.path.basename(filename).split('.')[-2])
                indices.append(index)
            except (ValueError, IndexError):
                continue
                
        return max(indices) if indices else -1

    def _generate_random_string(self):
        """Generate a cryptographically secure random string."""
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(self.random_length))

    def delete_files(self):
        """Delete all temporary files in the directory."""
        pattern = os.path.join(self.directory, f"{self.root}.*.{self.ext}")
        for filename in glob(pattern):
            os.remove(filename)
        self._current_index = -1
            
    def copy_last(self, dest):
        """Copy the last generated file to a destination."""
        if self._current_filename is None:
            raise ValueError("No files have been generated yet")
        os.system(f"cp {self._current_filename} {dest}")
        
    @property
    def next(self):
        """Generate the next filename in sequence."""
        self._current_index += 1
        filename = f"{self.root}.{self._current_index}.{self.ext}"
        self._current_filename = os.path.join(self.directory, filename)
        return self._current_filename

    @property
    def random(self):
        """Generate a random filename."""
        random_string = self._generate_random_string()
        filename = f"{self.root}.{random_string}.{self.ext}"
        self._current_filename = os.path.join(self.directory, filename)
        return self._current_filename

    @property
    def current_index(self):
        """Get the current index value."""
        return self._current_index

    @property
    def current(self):
        """Get the current filename."""
        return self._current_filename
    
# import random
# import string
# import os
# from typing import Optional

# def generate_random_filename(
#     extension: Optional[str] = 'csv',
#     length: Optional[int] = 10,
#     prefix: Optional[str] = 'data_',
#     directory: Optional[str] = '',
#     existing_check: Optional[bool] = True
# ) -> str:
#     """
#     Generate a random filename with optional parameters.
    
#     Args:
#         extension (str): File extension to append (e.g., '.txt', '.pdf')
#         length (int): Length of the random string (default: 10)
#         prefix (str): Prefix to add before the random string
#         directory (str): Directory path where the file will be created
#         existing_check (bool): Whether to check if filename already exists
    
#     Returns:
#         str: Generated filename
        
#     Raises:
#         ValueError: If length is less than 1
#         ValueError: If unable to generate unique filename after 100 attempts
#     """
#     if length < 1:
#         raise ValueError("Length must be at least 1")
        
#     # Clean up the extension
#     if extension and not extension.startswith('.'):
#         extension = '.' + extension
        
#     # Clean up the directory path
#     if directory:
#         directory = os.path.abspath(directory)
#         if not os.path.exists(directory):
#             os.makedirs(directory)
            
#     attempts = 0
#     max_attempts = 100
    
#     while True:
#         # Generate random string using ASCII letters and digits
#         random_string = ''.join(
#             random.choices(string.ascii_letters + string.digits, k=length)
#         )
        
#         # Combine all parts of the filename
#         filename = f"{prefix}{random_string}{extension}"
        
#         # Add directory path if specified
#         if directory:
#             filename = os.path.join(directory, filename)
            
#         # Check if file exists (if requested)
#         if not existing_check or not os.path.exists(filename):
#             return filename
            
#         attempts += 1
#         if attempts >= max_attempts:
#             raise ValueError(
#                 f"Unable to generate unique filename after {max_attempts} attempts"
#             )
