import os
from pathlib import Path

from .version import __version__

directory = str(Path(__file__).resolve().parent)

files = ['conopt464.dll', 'co4cclib64.dll', 'optconopt4.def']

file_paths = [directory + os.sep + file for file in files]
verbatim = 'CONOPT4 1 0 CO 1 0 2 LP RMIP NLP CNS DNLP RMINLP QCP RMIQCP\ngmsgennt.cmd\ngmsgennx.exe\nco4cclib64.dll co4 1 1'
