#!/usr/bin/env python3
# encoding:utf-8

import numpy as np

file1 = 'map_param.npz'
print(file1)

data = np.load(file1)
lst = data.files
for it in lst:
    print(data[it])

file2 = 'calibration_param.npz'
print(file2)

data2 = np.load(file2)
lst2 = data2.files
for it in lst2:
    print(data2[it])
