import logging


def check_internet_connection(host="8.8.8.8", port=53, timeout=1):
    """
    Checks whether the device is connected to the Internet by creating a socket
    connection with a host IP address. By default it makes a connection with
    Google's Public DNS Server on port 53.
    Source: https://stackoverflow.com/a/33117579

    Parameters:
    -----------
    host (str): host IP address, default="8.8.8.8"
    port (int): port number, default=53
    timeout(float, optional) = timeout in seconds, default=1

    Returns:
    --------
    bool
    """

    import socket

    logging.debug("Checking internet connection")
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as err:
        print(err)

    return False


def check_version():
    """
    Checks whether there is an update for this package.   
    """

    import sdownloader
    import requests

    current_version = sdownloader.__version__
    
    latest_version = requests.get("https://pypi.org/pypi/sdownloader/json")
    latest_version = latest_version.json()
    latest_version = latest_version["info"]["version"]

    if current_version == latest_version:
        logging.debug("The package is up to date.")
    elif current_version < latest_version:
        logging.debug("There is a newer version of this package.")
        message = """There is a newer version of this package.
You can update by simply typing `pip3 install --upgrade sdownloader`."""
        print(message)
    else:
        logging.debug("DEV version is in use.")