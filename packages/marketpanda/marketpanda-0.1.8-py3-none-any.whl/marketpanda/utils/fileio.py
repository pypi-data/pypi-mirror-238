# fileio.py
"""Helper function to save CSV data.
This contains a helper function for saving CSV files.
"""
import csv
import os
from pathlib import Path


def save_csv(failed_tickers, filename):
    """
    Save failed tickers as a csv to the directory where the
    app is running.

    Parameters
    ----------
    failed_tickers : 'list'
        A list of tickers that generated and error and historic
        price was not entered into the securities master database.
    filename : 'str'
        The filename of the csv being saved.
    """

    # File name for the qualifying loans CSV.
    output_path = Path(f"failed_inserts/{filename}.csv")

    # Save the qualifying loans in the current working directory.
    with open(output_path, 'w', newline='') as csvfile:
        # Create the csv writer object.
        csvwriter = csv.writer(csvfile)

        # Write the qualifying loans to the CSV file.
        for ticker in failed_tickers:
            csvwriter.writerow(ticker)
            

def get_file_metadata(file_path: str) -> dict:
    """
    Get the metadata of a file
    :param file_path: path to the file
    :return: dictionary containing the metadata
    """
    # Retrieve the metadata of the file
    file_metadata = os.stat(file_path)

    # Construct the metadata dictionary
    metadata = {
        "file_name": os.path.basename(file_path),
        "file_size in MB": file_metadata.st_size,
        "file_creation_time": file_metadata.st_ctime / ((1024 * 1024)),
        "file_modification_time": file_metadata.st_mtime
    }

    return metadata