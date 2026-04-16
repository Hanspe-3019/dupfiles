import os
from dataclasses import dataclass
from collections import defaultdict
import hashlib

from tqdm import tqdm

from . my_globals import OPT, sayit

@dataclass
class Fileinfo:
    """ DataClass FileInfo: path, size, ino
    """
    path: str
    size: int
    ino: int

    def hash_for_file(self):
        """
        Determine hash  checksum for a given file (first CHUNKSIZE Bytes)
        """
        try:
            with open(self.path, 'rb') as the_file:
                chunk = the_file.read(OPT.chunksize)
        except FileNotFoundError: # Temp File deleted?
            chunk = self.path
        return hash(chunk)

    def md5_for_file(self):
        """
        Determine the md5 checksum for a given file

        """
        md5 = hashlib.md5()
        with open(self.path, 'rb') as the_file:
            for chunk in iter(lambda: the_file.read(OPT.chunksize), b''):
                md5.update(chunk)
        return md5.hexdigest()

    @staticmethod
    def walk_tree(from_path):
        '''
        Walk the directory given by from_path, filtering as directed,
        appending them in dict size_to_files.
        '''
        size_to_files = defaultdict(list)
        sayit(f'walk start for {from_path:}')
        with tqdm(desc='Walking', unit=' Files') as t:
            num_files = 0
            for root, dirnames, files in os.walk(from_path, topdown=True):

                for cur_file in files:
                    t.update(1)
                    cur_path = os.path.join(root, cur_file)
                    try:
                        cur_size = os.lstat(cur_path).st_size
                    except FileNotFoundError:
                        cur_size = -1

                    if cur_size >= OPT.min_size:
                        num_files += 1
                        size_to_files[cur_size].append(
                            Fileinfo(
                                path=cur_path,
                                size=cur_size,
                                ino=os.lstat(cur_path).st_ino,
                            )
                        )
                    #
                #
                if len(OPT.excludes) > 0:
                    dirnames[:] = [
                        dir for dir in dirnames if dir not in OPT.excludes
                    ]
                dirnames[:] = [
                    dir for dir in dirnames
                        if not os.path.ismount(os.path.join(root, dir))
                ]

            t.set_postfix_str(
                f'collected {num_files} Files in {len(size_to_files)} Bins'
            )
        return size_to_files
