# dupfiles
Reports duplicate files in directory trees 
## Help
```bash
% python -m dupfiles -h
```
```
usage: python -m dupfiles [-h] [-s SIZE] [--chunk SIZE] [-v]
                          [--exclude [EXCLUDES ...]]
                          [DIRECTORY ...]

  Scans one or more directory trees for file duplicates and outputs
  their pathes groupwise to stdout. Example output:

   bin00000:     2956 "./condainstallinfo.ipynb"
   bin00000:     2956 "./.ipynb/condainstallinfo-checkpoint.ipynb"

  First col  : the group-id : f'grp{id:05d}'
  Second col : shows the file size
  Third col  : the path quoted with "

positional arguments:
  DIRECTORY             directory to be scanned, default current dir

options:
  -h, --help            show this help message and exit
  -s, --size SIZE       min size in bytes of files to check
  --chunk SIZE          Size of read chunks in bytes
  -v                    Verbose Flag
  --exclude [EXCLUDES ...]
                        Excluded directory names
```

## Run

```bash
% python -m dupfiles -s 10000  
```
```
17:13:02 – walk start for .
Walking: 19 Files [00:00, 57580.76 Files/s, collected 7 Files in 3 Bins]
Hashing: 5 of 5, 0.0s , finished
17:13:02 – Sum of duplicate sizes: 34604
bin00000:    17302 "./testfiles/test-N.txt"
bin00000:    17302 "./testfiles/test-M.txt"
bin00001:    17302 "./testfiles/test-A.txt"
bin00001:    17302 "./testfiles/test-B.txt"
17:13:02 – Found 2 groups of duplicate files
```

