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
                f"DIR: {path} is not a valid path")
        return path

    def human_size(hsize):
        '''  12G, 10K, 150, 3M -> Bytes
        '''
        try:
            the_bytes = int(hsize)
        except ValueError:
            the_digits, unit = hsize[:-1], hsize[-1]
            try:
                the_bytes = int(the_digits)
                if unit == 'K':
                    the_bytes *= 1024
                elif unit == 'M':
                    the_bytes *= 1024**2
                elif unit == 'G':
                    the_bytes *= 1024**3
                else:
                    raise ValueError
            except ValueError:
                raise argparse.ArgumentTypeError(
                        f'size {hsize} not recognized!')
            

        return the_bytes

    parser.add_argument(
        "-d", "--dump",
        action="store_true",dest="dump",
        help="Write bins to stdout"
    )

    parser.add_argument(
        "dirs",type=dir_path,
        nargs='*',
        default=[".",],
        help="directories to be scanned, default current dir",
        metavar="DIRs",
    )
    parser.add_argument(
        "-s",
        "--size",
        type=human_size,dest="min_size",
        default="250000",
        help="min size in bytes of files to check",
        metavar="SIZE",
    )
    parser.add_argument(
        "--chunk",
        type=human_size,dest="chunksize",
        default=8*1024,
        help="Size of read chunks in bytes, default 8K",
        metavar="CHUNK",
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
    parser.add_argument(
        "--debug",
        action="store_true",dest="debug",
        help="Debug Flag"
    )
    return parser.parse_args()

def sayit(text, prefix=None):
    ''' print mit Zeitstempel
    '''

    if prefix is None:
        prefix = time.strftime('%H:%M:%S')
    print(f"{prefix} – {text}", file=sys.stderr)

 
OPT = get_options()
if OPT.debug:
    sayit(OPT)
