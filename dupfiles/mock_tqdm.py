import time
import sys

class tqdm():
    ''' mocking the real tqdm
    '''
    def __init__(self, **args):

        self.desc = args.get('desc', 'Mocking tqdm')
        self.start = None
        self.postfix_str = ''
        self.total = 0
        pass
    def __enter__(self):
        print(self.desc, end=' ', file=sys.stderr)
        self.start = time.time()
        return self
    def __exit__(self, *args):
        print(f'{time.time() - self.start:.3f} sec for {self.total}, {self.postfix_str}', file=sys.stderr)
        pass
    def update(self, *args):
        self.total += args[0]
    def set_postfix_str(self, *args):
        self.postfix_str = args[0]
