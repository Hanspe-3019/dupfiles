import os
import sys
import time
import argparse

try:
    from tqdm import tqdm
except ImportError:
    from . mock_tqdm import tqdm
    print(tqdm().desc, file=sys.stderr)

def get_options():
    """ Options mit argparse
    """
    parser = argparse.ArgumentParser(
        # prog='dupefiles',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
          Scans one or more directory trees for file duplicates and optionally
          outputs bins of duplicates to stdout. Example output:

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
                the_bytes = int(the_digits) * 1000 ** ' KMG'.index(unit)
            except ValueError:
                raise argparse.ArgumentTypeError(
                        f'size {hsize} not recognized!')
        return the_bytes

    parser.add_argument(
        "-d", "--dump",
        nargs='?',
        default='',             # kein --dump      : kein dump 
        const='/**',            # --dump ohne GLOB : alles dumpen
        type=str,dest="dump",
        metavar='GLOB',

        help="Write bins to stdout, optionally filtered"
    )

    parser.add_argument(
        "dirs",type=dir_path,
        nargs='*',
        default=[".",],
        help="directories to be scanned, default current dir",
        metavar="DIRPATHes",
    )
    parser.add_argument(
        "-s",
        "--size",
        type=human_size,dest="min_size",
        default="0",
        help="min size in bytes of files to check",
        metavar="SIZE",
    )
    parser.add_argument(
        "--chunk",
        type=human_size,dest="chunksize",
        default=8*1024,
        help=argparse.SUPPRESS, # "Size of read chunks in bytes, default 8K",
        metavar="CHUNK",
    )
    parser.add_argument(
        "-v",
        action="store_true",dest="verbose",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "-e", "--excl",
        type=str,dest="excludes",
        nargs='*',
        default=[
            ".git",
            "Library",
        ],
        help="Excluded directory names, default .git and Library",
        metavar="DIR"
    )
    parser.add_argument(
        "-f", "--excl-files",
        type=str,dest="exclude_files",
        nargs='*',
        default=[
            ".DS_Store",
            ".gitignore",
        ],
        help="Excluded file names, default .DS_Store and .gitignore",
        metavar="DIR"
    )
    parser.add_argument(
        "--debug",
        action="store_true",dest="debug",
        help=argparse.SUPPRESS
    )
    return parser.parse_args()

def sayit(text, prefix=None):
    ''' print mit Zeitstempel
    '''

    if prefix is None:
        prefix = time.strftime('%H:%M:%S')
    print(f"{prefix:8s} – {text}", file=sys.stderr)

 
OPT = get_options()
if OPT.debug:
    sayit(OPT)
elif OPT.verbose:
    close = ":" if len(OPT.excludes) > 0 else "none"
    sayit(
        f'Excluded directory names {close}', prefix='verbose',
    )
    for name in OPT.excludes:
        sayit(f'\t{name}', prefix='verbose')
    close = ":" if len(OPT.exclude_files) > 0 else "none"
    sayit(
        f'Excluded file names {close}', prefix='verbose',
    )
    for name in OPT.exclude_files:
        sayit(f'\t{name}', prefix='verbose')
