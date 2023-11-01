import os
from pathlib import Path

from .version import __version__

directory = str(Path(__file__).resolve().parent)

files = ['libco4cclib64.so', 'libconopt464.so', 'optconopt4.def']

file_paths = [directory + os.sep + file for file in files]
verbatim = 'CONOPT4 1 0 CO 1 0 2 LP RMIP NLP CNS DNLP RMINLP QCP RMIQCP\ngmsgenus.run\ngmsgenux.out\nlibco4cclib64.so co4 1 1'
