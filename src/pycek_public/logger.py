import sys
import logging
import colorama
from colorama import Fore, Style

# Initialize colorama to work on Windows too
colorama.init()

# Define custom VERBOSE level (between DEBUG-10 and INFO-20)
VERBOSE = 15
logging.addLevelName(VERBOSE, 'VERBOSE')
RESULT = 25
logging.addLevelName(RESULT, 'RESULT')

class ColoredFormatter(logging.Formatter):
    """Custom formatter that adds colors to log messages based on level with fixed width"""
    COLORS = {
        'DEBUG': Fore.CYAN + Style.BRIGHT,
        'VERBOSE': Fore.BLUE + Style.BRIGHT,
        'INFO': Fore.GREEN + Style.BRIGHT,
        'RESULT' : Fore.RESET + Style.BRIGHT,
        'WARNING': Fore.YELLOW + Style.BRIGHT,
        'ERROR': Fore.RED + Style.BRIGHT,
        'CRITICAL': Fore.MAGENTA + Style.BRIGHT
    }
    LEVEL_NAME_WIDTH = 8

    def format(self, record):
        # Save original levelname and message
        orig_levelname = record.levelname
        orig_msg = record.msg

        # Determine the color for the level
        color_code = self.COLORS.get(orig_levelname, '')

        # Calculate padding for levelname
        padding = ' ' * (self.LEVEL_NAME_WIDTH - len(orig_levelname))

        # Apply color to levelname with padding
        record.levelname = f"{color_code}{orig_levelname}{padding}{Style.RESET_ALL}"

        # Apply color to the message as well
        record.msg = f"{color_code}{orig_msg}{Style.RESET_ALL}"

        # Format the message
        result = super().format(record)

        # Restore original values
        record.levelname = orig_levelname
        record.msg = orig_msg
        return result
    
class ColoredLogger(logging.Logger):
    """Custom logger class with verbose method"""
    
    def verbose(self, msg, *args, **kwargs):
        """Log at custom VERBOSE level"""
        if self.isEnabledFor(VERBOSE):
            self._log(VERBOSE, msg, args, **kwargs)
            
    def result(self, msg, *args, **kwargs):
        """Log at custom RESULT level"""
        if self.isEnabledFor(RESULT):
            self._log(RESULT, msg, args, **kwargs)
            
    # logging.Logger.result = custom_logging

def setup_logger(name='colored_logger', level="INFO"):
    """Set up and return a colored logger instance"""
    
    # Register our custom logger class
    logging.setLoggerClass(ColoredLogger)
    
    # Create logger
    logger = logging.getLogger(name)
    
    # Set logger level
    try:
        logger.setLevel(getattr(logging, level.upper()))
    except AttributeError:
        logger.setLevel(logging.INFO)  # Default to INFO if invalid level
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # Create formatter
    formatter = ColoredFormatter(
        # fmt='%(asctime)s - %(levelname)s - %(message)s',
        # datefmt='%Y-%m-%d %H:%M:%S'
        fmt='%(levelname)8s - %(message)s'
    )
    
    # Add formatter to handler
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    return logger

# Example usage
if __name__ == '__main__':
    logger = setup_logger()
    
    # Test all log levels including new VERBOSE level
    logger.debug("This is a debug message")
    logger.verbose("This is a verbose message")  # New verbose level
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
