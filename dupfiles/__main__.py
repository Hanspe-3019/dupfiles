"""
Find duplicate files from a given root in the directory hierarchy
of a given size

https://github.com/mumbly/PyUtils/blob/master/FileDupeFinder.py

"""
from collections import defaultdict

from tqdm import tqdm

from . my_globals import OPT, sayit
from . fileinfo import Fileinfo
from . finddupes import get_dupgroups

#[default: '{l_bar}{bar}{r_bar}'], where
#    l_bar='{desc}: {percentage:3.0f}%|' and
#    r_bar='| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, '
#        '{rate_fmt}{postfix}]'

FORMAT= '{desc}: {n_fmt} of {total_fmt}, {elapsed_s:.1f}s {postfix}'

class FileDupes:
    """Container for the list of dupe files"""

    def __init__(
        self,
        ):

        size_to_files = defaultdict(list)

        for root in OPT.dirs:
            for size, files in  Fileinfo.walk_tree(root).items():
                size_to_files[size].extend(files)

        self.bins = []
        with tqdm(desc='Hashing', bar_format=FORMAT, miniters=1) as progress_bar:

            progress_bar.total = sum(
                len(files) for files in size_to_files.values()
                    if len(files) > 1
            )

            for filesize, files in size_to_files.items():
                if len(files) <= 1:
                    continue
                progress_bar.set_postfix_str(f'{filesize} x {len(files)}')
                if len(files) > 1:
                    self.bins.extend(get_dupgroups(files, progress_bar))

            progress_bar.set_postfix_str('finished')


    def print_dupgroups(self):
        """ Ausgabe der ermittelten Duplikatgruppen auf stdout
        """
        for i, bin in enumerate(self.bins):
            for fileinfo in bin:
                print(
                    f'bin{i:05d}:{fileinfo.size:9d} "{fileinfo.path}"'
                )
        sayit(f"Found {len(self.bins)} groups of duplicate files")
    def print_statistics(self):
        """
        Ausgabe von Statistiken
        """
        dup_sizes = 0
        for bin in self.bins:
            size = bin[0].size
            dup_sizes += size * (len(bin) - 1)
        sayit(f"Sum of duplicate sizes: {dup_sizes}")



def main():
    """ Hier geht es los
    """
    dupes = FileDupes()
    dupes.print_statistics()
    dupes.print_dupgroups()

if __name__ == '__main__':
    main()
