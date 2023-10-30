import requests
import os
import logging
import tarfile
import shutil


SOURCE_URL = "https://sparse.tamu.edu/"


def format_matrix_names(matrix_list=None):
    """
    Formats matrix names.

    Parameters:
    -----------
    matrix_list (list): matrix names to parse.

    Returns:
    --------
    matrices (list): formatted data.
    """

    if not matrix_list:
        logging.critical("`matrix_list` in fetch.format_matrix_names is None!")
        raise SystemExit("`matrix_list` in fetch.format_matrix_names can not be None.")

    matrices = [tuple(matrix.split('/')) for matrix in matrix_list]
    return matrices


def read_matrix_names(data=None, data_type=None):
    """
    Reads matrix names from given source and parses them to
    a suitable format.

    Parameters:
    -----------
    data (string): source data.
    data_type (string): type of `data`. Values: `file` or `list.

    Returns:
    --------
    matrices (list): contains tuples that hold group and matrix names.
    """

    def read_from_file(path):
        if not os.path.exists(data):
            logging.critical("List file couldn't found exiting...")
            raise SystemExit()
        
        with open(data) as list_file:
            matrices = list_file.read().splitlines()
        return matrices

    def read_from_list(m_list):
        if str.endswith(m_list, ";"):
            m_list = m_list[:-1]

        matrices = m_list.split(";")
        return matrices

    if not data_type:
        logging.warning("`data_type` in `read_matrix_names` is None!")
    if not data:
        logging.critical("`data` in `read_matrix_names` is None!")
        raise SystemExit("`data` in `read_matrix_names` can not be None.")

    if data_type == "file":
        logging.debug("Reading matrix names from " + data)
        data = read_from_file(data)
        
    elif data_type == "list":
        logging.debug("Reading matrix names from given list")
        data = read_from_list(data)

    matrices = format_matrix_names(data)
    return matrices


def download_data_files(matrix_list, destination=None, keep_archive_files=False):
    """
    Downloads the given list of matrices from SparseSuit Collection.

    Parameters:
    -----------
    matrix_list (array[][]<string>): matrix groups and names
    destination (string, optional): root dir path of data files, default=None
    keep_archive_files (bool, optinal): to save or remove downloaded archive files
                                        default=False
    """
    
    if not destination:
        destination = './'
        logging.info("`destination` paramater isn't provided. Downloading to `./`")

    os.makedirs('./archive', exist_ok=True)

    file_list = []
    err = 0

    for item in matrix_list:
        matrix_name = item[0] + '_' + item[1]
        matrix_url = SOURCE_URL + 'MM' + '/' + item[0] + '/' + item[1] + '.tar.gz'
        matrix_archive = requests.get(matrix_url)

        if matrix_archive.status_code == 200:
            tmp = './archive/' + matrix_name + '.tar.gz'
            with open(tmp, 'wb') as f:
                f.write(matrix_archive.content)
            file_list.append(tmp)
            print(matrix_name, "downloaded.")
            logging.debug(matrix_name + " downloaded.")
        else:
            err += 1
            print(matrix_name, "couldn't download!")
            logging.warning(matrix_name + " couldn't download!")

    if not err:
        logging.info("Archive files downloaded successfully.")
    else:
        logging.info(err + " error(s) occured during download.")

    extract_archive_files(file_list, destination)

    if not keep_archive_files:
        shutil.rmtree('./archive')
        logging.info('Archive files deleted.')


def extract_archive_files(file_list, destination=None):
    """
    Extract downloaded archive files.

    Parameters:
    -----------
    file_list (string): list of archive files
    destination (string, optional): a path for extracting the archives into, default=None
    """

    for f in file_list:
        with tarfile.open(f, "r:gz") as tar:
            tar.extractall(path=destination)
            logging.debug("`" + f + '` extracted to ' + destination)

    logging.info("Archive files extracted to: " + destination)
