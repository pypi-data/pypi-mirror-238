import os
from .utils import get_file_metadata
import gdown

def download_db(data_folder="../../data"):
    """
    Download database from google drive
    :param data_folder: root directory to save database. Default: ../../data
    :return: full path to downloaded database.
    """
    url = 'https://drive.google.com/uc?id=1HiBvyOnzTi0kXY7GBSZ2RcwsdxJI90yr'
    filename = "marketvault.db"
    output_full = os.path.abspath(os.path.join(data_folder, filename))

    # create google drive downloader object
    gdown.download(url, output_full, quiet=False)

    print(get_file_metadata(output_full))
    return output_full