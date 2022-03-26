import coloredlogs
import logging

import sys
import platform
from subprocess import Popen

program_log = logging.getLogger(__name__)

log_file = logging.FileHandler("log.log",'w', 'utf-8')
log_file.setLevel(logging.DEBUG)
program_log.setLevel(logging.DEBUG)
fileformat = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s",datefmt="%H:%M:%S")
log_file.setFormatter(fileformat)
program_log.addHandler(log_file)

stream = logging.StreamHandler()
stream.setLevel(logging.DEBUG)
streamformat = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
stream.setFormatter(streamformat)
