import os
import sys
import time
import shutil
import random
import math

from pathlib import Path
from datetime import datetime

script_path = Path(os.getcwd())

class DataGenerator():
    @staticmethod
    def getC0DE(times = 1):
        if times <= 0:
            raise Exception("error: bytes given times is not valid!")
        return bytes([0xC0, 0xDE]) * math.floor(times / 2)

def delete_existing_folders_in(dst: Path, starting_with = ""):
    for item in dst.rglob("*"):
        relative_item_path = str(item.relative_to(dst))

        if not item.is_dir():
            continue
        
        if relative_item_path.startswith(".git"):
            continue
    
        if relative_item_path.startswith(starting_with):
            print("* delete: " + relative_item_path)
            shutil.rmtree(item)

def write_some_files_to(dst: Path, filetype="raw", amount=1, size=1):
    for count in range(0, amount):
        dst_file_name = "file_" + str(count+1) + "_" + str(datetime.now().strftime("%y%m%d_%H%M%S")) + "." + filetype

        dst_file = dst / dst_file_name

        random_waiting_seconds = random.randint(0, 3)
        print("* random waiting for " + str(random_waiting_seconds) +  " secs ...")
        time.sleep(random_waiting_seconds)

        if not dst_file.is_file():
            dst_file.write_bytes(DataGenerator.getC0DE(times = size))

def wait_for_secs(secs):
    for _ in range(0, secs):
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\n")

def main():
    if not script_path.is_dir():
        raise Exception("error: path does not exists")

    print("* cleaning up ...")
    delete_existing_folders_in(script_path, starting_with="tmp_")

    dst_directory = script_path / str("tmp_" + str(datetime.now().strftime("%y%m%d_%H%M%S")))

    if not dst_directory.is_dir():
        dst_directory.mkdir()

    print("* writing to " + str(dst_directory))

    write_some_files_to(dst_directory, filetype="raw", amount = 3, size = 1024)

    print("* done!")

if __name__ == "__main__":
    main()


