import time
import os
import sys
print(1)
out_dir = r'D:\Documents\dump'
time.sleep(20)
print(2)
time.sleep(20)
out_file = os.path.join(out_dir, str(time.time()))
print(3)
time.sleep(20)
with open(out_file, 'w') as out:
    pass
print(4)
time.sleep(20)
sys.exit(0)