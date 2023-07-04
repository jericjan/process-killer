import argparse
import logging
import os
import sys
from pathlib import Path

import psutil

parser = argparse.ArgumentParser()
parser.add_argument(
    "process_names", nargs="+", help="One or more names of processes (with .exe)"
)
args = parser.parse_args()

processes = args.process_names

current_dir = Path(sys.executable).parent if hasattr(sys, "frozen") else Path.cwd()


logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)
log_file = current_dir / "process_killer.log"
file_handler = logging.FileHandler(log_file)
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def kill_processes_by_name(process_name):
    count = 0
    for proc in psutil.process_iter(["pid", "name"]):
        if proc.info["name"] == process_name:
            proc.kill()
            logger.info(f"{process_name} [{proc.info['pid']}] killed!")
            count += 1
    return count


logger.info("Starting process killer...")
# Usage example

total_kill_count = 0
for process in processes:
    logger.info(f"Looking for {process}...")
    kill_count = kill_processes_by_name(process)
    total_kill_count += kill_count

logger.info(f"Finished process killer... {total_kill_count} killed")
