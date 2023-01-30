import os
import sys
import time
import shutil
import random

from pathlib import Path
from datetime import datetime

script_path = Path(os.getcwd())

def wait_for_secs(secs):
    for _ in range(0, secs):
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\n")

if not script_path.is_dir():
    raise Exception("error: path does not exists")

dst_directory = script_path / str("tmp_" + str(datetime.now().strftime("%y%m%d_%H%M%S")))

if not dst_directory.is_dir():
    dst_directory.mkdir()


print("* writing to " + str(dst_directory))

wait_for_secs(3)
print("* cleaning up")

if dst_directory.exists():
    shutil.rmtree(dst_directory)

print("* done!")


