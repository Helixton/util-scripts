import os
import sys
import argparse
import time
import shutil
import random
import math

from pathlib import Path
from datetime import datetime



class DataGenerator():
    @staticmethod
    def getC0DE(times = 1):
        if times <= 0:
            raise Exception("error: bytes given times is not valid!")
        return bytes([0xC0, 0xDE]) * math.ceil(times / 2)

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

        random_waiting_seconds = random.randint(0, 2)
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

    parser = argparse.ArgumentParser()

    parser.add_argument("-b", "--basedirectory", help="", default=Path(os.getcwd()), type=Path, required=False)
    parser.add_argument("-a", "--amount", help="", default=1, type=int, required=False)
    parser.add_argument("-f", "--filesize", help="", default=1, type=int, required=False)
    parser.add_argument("-c", "--cleanup", help="", default=False, required=False, action="store_true")

    args = parser.parse_args()

    base_directory = args.basedirectory
    amount = args.amount
    file_size = args.filesize
    is_cleanup = args.cleanup

    if not base_directory.is_dir():
        raise Exception("error: path does not exists")

    if is_cleanup:
        print("* cleaning up ...")
        delete_existing_folders_in(base_directory, starting_with="tmp_")

    target_directory = base_directory / str("tmp_" + str(datetime.now().strftime("%y%m%d_%H%M%S")))

    if not target_directory.is_dir():
        target_directory.mkdir()

    print("* writing to " + str(target_directory))

    write_some_files_to(target_directory, filetype="raw", amount = amount, size = file_size)

    print("* done!")

if __name__ == "__main__":
    main()


