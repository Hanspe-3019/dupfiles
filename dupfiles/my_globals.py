import os
import sys
import time
import argparse

def get_options():
    """ Options mit argparse
    """
    parser = argparse.ArgumentParser(
        # prog='dupefiles',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
          Scans one or more directory trees for file duplicates and outputs
          their pathes groupwise to stdout. Example output:

           bin00000:     2956 "./condainstallinfo.ipynb"
           bin00000:     2956 "./.ipynb/condainstallinfo-checkpoint.ipynb"

          First col  : the group-id : f'grp{id:05d}'
          Second col : shows the file size
          Third col  : the path quoted with "
        """.replace(' '*8, '')
    )

    def dir_path(path):
        """ Validate Directory
        """
        if not os.path.isdir(path):
            raise argparse.ArgumentTypeError(
                f"readable_dir:{path} is not a valid path")
        return path

    parser.add_argument(
        "dirs",type=dir_path,
        nargs='*',
        default=[".",],
        help="directory to be scanned, default current dir",
        metavar="DIRECTORY",
    )
    parser.add_argument(
        "-s",
        "--size",
        type=int,dest="min_size",
        default="250000",
        help="min size in bytes of files to check",
        metavar="SIZE",
    )
    parser.add_argument(
        "--chunk",
        type=int,dest="chunksize",
        default=8*1024,
        help="Size of read chunks in bytes",
        metavar="SIZE",
    )
    parser.add_argument(
        "-v",
        action="store_true",dest="verbose",
        help="Verbose Flag"
    )
    parser.add_argument(
        "--exclude",
        type=str,dest="excludes",
        nargs='*',
        default=[
            "Backups.backupdb",
            ".git",
            ".svn",
            "Library",
        ],
        help="Excluded directory names",
    )
    return parser.parse_args()

def sayit(text):
    ''' print mit Zeitstempel
    '''
    print(f"{time.strftime('%H:%M:%S')} – {text}", file=sys.stderr)

 
OPT = get_options()
if OPT.verbose:
    sayit(OPT)
