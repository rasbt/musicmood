# Sebastian Raschka
# Script to generate a random collection of n items from
# the million song dataset directory tree.
#
# Python 3 script
#
# Usage:
# Modify lines at the bottom 
#  - to adjust the sample size n (= number output files).
#  - to set the input and output directories
#
# Then run:
#      python get_random_subset.py

import glob
import fileinput
import sys
import os
import random
import shutil

def collect(cur_dir, collection):
    filenames = glob.glob(os.path.join(cur_dir,'*'))
    for f in filenames:
        if f.endswith('.h5'):
            collection.append(f)

def run(cur_dir, collection):
    tree = os.walk(cur_dir)
    for d in tree:
        collect(cur_dir=d[0], collection=collection)
    return collection

def gen_random_sample(n, collection):
    rand_sample = set()
    total = len(collection)
    while len(rand_sample) < n:
        rand_idx = random.randint(0, total-1)
        rand_sample.add(collection[rand_idx])
    return rand_sample

def copy(rand_sample, target_dir):
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    for src in rand_sample:
        shutil.copyfile(src, os.path.join(target_dir,os.path.basename(src)))

if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(
        description='A command line tool to select random subsamples of the Million Song dataset.',
        formatter_class=argparse.RawTextHelpFormatter
        )


    parser.add_argument('in_dir', help='Input directory')
    parser.add_argument('out_dir', help='Output directory')

    parser.add_argument('-n',  help='Sample size for the subsample')
    parser.add_argument('-v', '--version', action='version', version='v. 1.0')

    args = parser.parse_args()

    n = int(args.n)
        
    random.seed(123)
    collection = []
    collection = run(args.in_dir, collection)
    rand_sample = gen_random_sample(n=n, collection=collection)
    copy(rand_sample, args.out_dir)
