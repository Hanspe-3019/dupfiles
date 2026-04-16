from collections import defaultdict

from . my_globals import OPT

def get_dupgroups(fileinfos, progress_bar):
    '''get list of Fileinfo of files of equal size
    compute hash to eliminate false positives from list
    returns list of groups of equal files.

    First use pythons hash over the first chunk
    if different: done
    Second compute md5 over whole file
    '''
    #
    # dict hash auf Liste von Fileinfos
    # hash ist zunächst der der Python-Hash auf den Chunk
    # Wenn der Chunk-Hash bereits eindeutig ist, sparen wir
    # uns bei großen Files die Berechnung des md5 über den gesamten File
    #
    min_size = min(file.size for file in fileinfos)
    size =     max(file.size for file in fileinfos)
    if size != min_size:
        raise AssertionError(f'Sizes not equal! {min_size} != {size}')

    hash_to_file = defaultdict(list)

    for fileinfo in fileinfos:
        the_hash = fileinfo.hash_for_file()
        hash_to_file[the_hash].append(fileinfo)
        progress_bar.update(1)

    if size > OPT.chunksize:
        # Wir haben nur Hash über den ersten Chunk gebildet
        # Jetzt also noch mal für den Rest ein voller md5-Hash:
        md5_to_file = defaultdict(list)
        for files in hash_to_file.values():
            if len(files) == 1:
                continue
            for fileinfo in files:
                the_hash = fileinfo.md5_for_file()
                md5_to_file[the_hash].append(fileinfo)

        groups_of_dups = [
            files for files in md5_to_file.values()
                if len(files) > 1
        ]
    else:
        groups_of_dups = [
            files for files in hash_to_file.values()
                if len(files) > 1
        ]

    return groups_of_dups

