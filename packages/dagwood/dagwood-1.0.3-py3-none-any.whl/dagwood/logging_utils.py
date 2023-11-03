import logging
import os
from datetime import datetime

def setup_logging(
        folder_name:str = 'logs', 
        file_name:str = None, 
        level:int = logging.INFO, 
        format:str = '%(asctime)s - %(levelname)s - %(message)s'
    ) -> logging.Logger:
    """
    Set up logging for the script.

    Parameters
    ----------
    folder_name : str, optional
        The name of the folder to store the log files in, by default 'logs'
    file_name : str, optional
        The name of the log file, by default None
    level : int, optional
        The logging level, by default logging.INFO
    format : str, optional
        The logging format, by default '%(asctime)s - %(levelname)s - %(message)s'
    
    Returns
    -------
    logging.Logger
        The logger instance.
    """
    # Create log directory if it doesn't exist
    log_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), folder_name)
    os.makedirs(log_directory, exist_ok=True)

    # Set up logger
    logger = logging.getLogger()
    logger.setLevel(level)

    # Set up formatter
    formatter = logging.Formatter(format)

    # Set up stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # Check if file name is provided
    if not file_name:
        file_name = f'{datetime.utcnow().strftime("%Y%m%d%H%M%S")}.log'

    # Set up file handler
    log_file = os.path.join(log_directory, file_name)

    # Check if file exists
    file_handler = logging.FileHandler(filename=log_file)  # Store file handler as instance variable
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Return logger
    return logger
