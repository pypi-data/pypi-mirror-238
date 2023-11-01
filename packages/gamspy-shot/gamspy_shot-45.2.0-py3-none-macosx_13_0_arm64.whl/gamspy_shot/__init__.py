import os
from pathlib import Path

from .version import __version__

directory = str(Path(__file__).resolve().parent)

files = ['libshtcclib64.dylib', 'libipopt64.dylib', 'libgurobi100.dylib']

file_paths = [directory + os.sep + file for file in files]
verbatim = 'SHOT 1001 5 000102030405 1 0 2 MINLP MIQCP\ngmsgenus.run\ngmsgenux.out\nlibshtcclib64.dylib sht 1 1'
