import os
import shutil

import errno


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def rm_rf(path):
    if os.path.exists(path):
        shutil.rmtree(path)
