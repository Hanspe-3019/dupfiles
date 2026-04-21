"""
Find duplicate files from a given root in the directory hierarchy
of a given size

https://github.com/mumbly/PyUtils/blob/master/FileDupeFinder.py

"""
from collections import defaultdict

from . my_globals import tqdm
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


    def print_dupgroups(self, glob):
        """ Ausgabe der ermittelten Duplikatgruppen auf stdout
        """
        for i, the_bin in enumerate(self.bins):
            if not any( fileinfo.matches(glob) for fileinfo in the_bin ):
                continue
            for fileinfo in the_bin:
                print(
                    f'bin{i:05d}:{fileinfo.size:9d} "{fileinfo.path}"'
                )
        sayit(f"Found {len(self.bins)} groups of duplicate files")
    def print_statistics(self):
        """
        Ausgabe von Statistiken
        """
        dup_sizes = 0
        dir_to_others = defaultdict(set)
        for the_bin in self.bins:
            size = the_bin[0].size
            dup_sizes += size * (len(the_bin) - 1)
            dirs = set(
                fileinfo.path.parent for fileinfo in the_bin
            )
            for the_dir in dirs:
                for other in dirs:
                    if other != the_dir: 
                        dir_to_others[the_dir].add(other)


        sayit(f"Sum of duplicate's sizes: {dup_sizes}", prefix='Stats  A')

        files_in_dir = Fileinfo.get_files_in_dir()
        dups_in_dir = defaultdict(int)

        for the_bin in self.bins:
            for fileinfo in the_bin:
                its_dir = fileinfo.path.parent
                dups_in_dir[its_dir] += 1

        indent = ' '*10 + '-> '
        for the_dir, dups in dups_in_dir.items():

                its_count_of_files = files_in_dir[the_dir]
                sayit(
                    f'{dups:6d}'
                    f'{its_count_of_files:6d}'
                    f' {the_dir}',
                    prefix='Stats  B',
                )
                for other in dir_to_others[the_dir]:
                    sayit(f'{indent}{other}', prefix='Stats  B')



def main():
    """ Hier geht es los
    """
    dupes = FileDupes()
    dupes.print_statistics()
    if OPT.dump != '':
        dupes.print_dupgroups(OPT.dump)

if __name__ == '__main__':
    main()
