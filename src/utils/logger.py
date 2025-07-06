import logging

def setup_logging(log_file="src.log"):
    """Set up logging configuration with file and console output.

    Configures logging to write to both a file and the console with a
    specified format and INFO level.

    Args:
        log_file (str, optional): Path to the log file. Defaults to "src.log".

    Returns:
        logging.Logger: Configured logger instance.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )    
    return logging.getLogger(__name__)
