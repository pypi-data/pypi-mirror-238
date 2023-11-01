import os
import sys
import subprocess


out1 = subprocess.check_output([sys.executable, 'test.py'])
subprocess.check_call(['g++', '-o', 'test', 'test.cpp', '-lm'])
out2 = subprocess.check_output(['./test'])

out1 = out1.decode()
out2 = out2.decode()

out1 = out1.split('\n')
out2 = out2.split('\n')
data1, data2 = [], []
for o1,o2 in zip(out1, out2):
    try:
        i1, v1 = o1.split(':')
        i2, v2 = o2.split(':')
    except ValueError:
        continue
    i1 = int(i1)
    i2 = int(i2)
    v1 = float(v1)
    v2 = float(v2)
    data1.append(v1)
    data2.append(v2)
    s = max([abs(v1),abs(v2)])
    if s == 0:
        s = 1
        
    print(i1, i2, v1, v2, '->', abs(v1-v2)/s)


import pylab
pylab.plot(data1, marker='x')
pylab.plot(data2, marker='x')
pylab.show()
