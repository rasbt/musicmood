# Sebastian Raschka
# Script to partition the filtered dataset 
# Sebastian Raschka
#
# splitting HDF5 dataset into training and validation datasets
#
# Python 3 script
#


import glob
import fileinput
import sys
import os
import random
import shutil

import argparse

parser = argparse.ArgumentParser(
        description='A command line tool for splitting HDF5 dataset into training and validation datasets.',
        formatter_class=argparse.RawTextHelpFormatter
        )

parser.add_argument('in_dir', help='Input directory')
parser.add_argument('-o1', '--out_dir1', help='Output directory 1')
parser.add_argument('-o2', '--out_dir2', help='Output directory 2')
parser.add_argument('-n', '--number', help='Number of files that should go into out_dir1, rest goes in out_dir2.')
parser.add_argument('-v', '--version', action='version', version='v. 1.0')

args = parser.parse_args()


for d in [args.out_dir1, args.out_dir2]:
    if not os.path.exists(d):
        os.makedirs(d)


in_paths = [os.path.join(args.in_dir, f) for f in  os.listdir(args.in_dir)]

total = len(in_paths)


out_paths1 = [os.path.join(args.out_dir1, f) for f in  os.listdir(args.in_dir)]
out_paths2 = [os.path.join(args.out_dir2, f) for f in  os.listdir(args.in_dir)]


k = total-int(args.number)
while len(in_paths) > k:
    idx = random.randint(0,len(in_paths)-1)
    shutil.copyfile(in_paths[idx], out_paths1[idx])
    in_paths.pop(idx)
    out_paths1.pop(idx)

while len(in_paths) > 0:
    idx = random.randint(0,len(in_paths)-1)
    shutil.copyfile(in_paths[idx], out_paths2[idx])
    in_paths.pop(idx)
    out_paths2.pop(idx)

    

