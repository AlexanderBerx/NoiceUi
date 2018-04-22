import time
import os
import sys
print(1)
out_dir = r'D:\Documents\dump'
print(2)
out_file = os.path.join(out_dir, str(time.time()))
print(3)
with open(out_file, 'w') as out:
    pass
print(4)
time.sleep(30)
sys.exit(0)