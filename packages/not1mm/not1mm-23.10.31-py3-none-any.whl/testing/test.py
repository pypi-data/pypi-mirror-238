"""doc"""

import psutil

for proc in psutil.process_iter():
    if len(proc.cmdline()) == 2:
        print(proc.cmdline()[1])
