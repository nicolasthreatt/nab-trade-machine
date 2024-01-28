import os
import sys

def report_error(team: str, limit: float, contract: float) -> None:
    """Report error and exit program.

    Parameters:
        team (str): Team name.
        limit (float): Maximum amount.
        contract (float): Contract amount.
    """
    # Convert floating-point numbers to formatted strings
    limit_str = f"{limit:,.2f}"
    contract_str = f"{contract:,.2f}"

    # Construct error message for log file
    error_message = f"{team} can only take up to ${limit_str}. Cannot take contract ${contract_str}."
    print(error_message)
    
    # Get current directory
    current_directory = os.getcwd()
    
    # Define logs subdirectory path
    logs_directory = os.path.join(current_directory, "logs")
    
    # Create logs subdirectory if it doesn't exist
    os.makedirs(logs_directory, exist_ok=True)
    
    # Define log file path
    log_file_path = os.path.join(logs_directory, "error.log")

    # Write error message to log file
    with open(log_file_path, "a") as log_file:
        log_file.write(log_error_message + "\n")
    
    # Exit program
    sys.exit("Trade unable to be processed")
