# use curl -X POST localhost:4221/files/test.txt -d "working"
# on running the code use main.py --directory #the path of the directory

import io
import gzip
import binascii

file = gzip.compress('foo'.encode())
print(len(file))
print(file)