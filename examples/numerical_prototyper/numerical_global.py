import os
import errno


def ensurePathExists(path):
    try:
        path = os.path.join(path, "")
        directory = os.path.dirname(path)
        os.makedirs(directory)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
