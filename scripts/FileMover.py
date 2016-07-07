#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function

locs = {"PSI" : ["root://192.33.123.24:1094/", ""],
        "Pisa" : ["root://stormgf2.pi.infn.it:1094/","/gpfs/ddn/srm/cms"]}

import os
import argparse

parser = argparse.ArgumentParser(prog='FileMover')
parser.add_argument('--loc', required=True, type=str, choices=locs.keys())
parser.add_argument('--path', required=True, type=str)
parser.add_argument('--datasets', nargs='+', type=str, default=[])
parser.add_argument('--out_dir', type=str, default=os.getcwd()+"/")
parser.add_argument('--test_run', action='store_true')

args = parser.parse_args()

from XRootD.client.flags import DirListFlags, OpenFlags, MkDirFlags, QueryCode
from XRootD import client
from mut_framework.mut_transfer.folder_transfer import DataSource,natural_sort

c =  DataSource("".join(locs[args.loc])+args.path)

if len(args.datasets) is 0:
    status, listing = c.dirlist(locs[args.loc][1]+args.path,DirListFlags.STAT)
    for entry in listing:
        print("{0} {1:>10} {2}".format(entry.statinfo.modtimestr,
                entry.statinfo.size, entry.name))
 

for dataset in args.datasets:
    print("coping folder {0} ... ".format(dataset), end="")
    if not os.path.exists(dataset):
        os.makedirs(dataset)
    c.copy_all_root_files(dataset, args.out_dir+dataset, test_run = args.test_run)
    print("DONE")
