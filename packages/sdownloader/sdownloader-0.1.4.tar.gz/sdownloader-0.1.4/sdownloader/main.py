import argparse
import logging
import os
from . import fetch, utils, __version__

def main():
    parser = argparse.ArgumentParser(
        prog="sdownloader", 
        description="Data downloader from SparseSuite.")
    
    source_args_group = parser.add_mutually_exclusive_group(required=True)
    source_args_group.add_argument("-f", "--list-file", help="matrix name list file destination.")
    source_args_group.add_argument("-m", help="matrix names. Example: `sdownloader -m \"HB/1138_bus;FIDAP/ex37\"`")

    parser.add_argument("-d", "--destination",
                        help="destination path. Optional, default=current working directory.",
                        default=os.getcwd())
    parser.add_argument("-v", "--verbose", help="toggle verbose mode.", action="store_true")
    parser.add_argument('-V', '--version', action='version', version="%(prog)s ("+__version__+")")

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level = logging.INFO,
                            format="[%(asctime)s]:%(levelname)s:%(message)s",
                            datefmt='%H:%M:%S')

    if not utils.check_internet_connection():
        logging.critical("Can not connect to the Internet")
        raise SystemExit("Can not connect to the Internet, please check your connection. Exiting...")

    #utils.check_version()
    
    if args.list_file:
        matrices = fetch.read_matrix_names(args.list_file, "file")
    else:
        matrices = fetch.read_matrix_names(args.m, "list")

    fetch.download_data_files(matrices, destination=args.destination, keep_archive_files=False)

if __name__ == "__main__":
    main()