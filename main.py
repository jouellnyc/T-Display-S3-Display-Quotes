""" S3-T-Display is finicky and can lock up forever w/o a short sleep """
import time
print("Sleeping")
time.sleep(3)

import os
from common import setup_file, quotes_dir

def file_or_dir_exists(filename):
    try:
        os.stat(filename)
    except OSError:
        return False
    else:
        return True
    
if not file_or_dir_exists(setup_file):
    import setup
    import gc
    gc.collect()
    import setup.setup
    import setup.microdot_runner
else:
    import gc
    gc.collect()
    import quote_app.quote_runner    