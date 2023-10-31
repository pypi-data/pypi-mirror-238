from .utils import get_file_metadata
import gdown

def download_db(root_dir="../../data"):
    """
    Download database from google drive
    :return: database binary file
    """
    url = 'https://drive.google.com/uc?id=1HiBvyOnzTi0kXY7GBSZ2RcwsdxJI90yr'
    output = "marketvault.db"
    output_full = f"{root_dir}/{output}"

    # create google drive downloader object
    gdown.download(url, output_full, quiet=False)
    print(get_file_metadata(output))
    return output_full