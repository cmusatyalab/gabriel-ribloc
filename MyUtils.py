import logging
import sys

custom_logger_level=logging.DEBUG
formatter = logging.Formatter('%(asctime)-15s %(levelname)-8s %(processName)s %(message)s')  
LOG=logging.getLogger(__name__)
LOG.setLevel(custom_logger_level)
ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(formatter)
LOG.addHandler(ch)

import time                                                
def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
 
        LOG.debug('%r %.1f ms' % \
                  (method.__name__, (te-ts)*1000))
        return result
    return timed
