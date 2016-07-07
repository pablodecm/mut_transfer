
from __future__ import print_function

from XRootD import client
from XRootD.client.flags import DirListFlags

import re

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)


class DataSource(client.FileSystem):
    def __init__(self, url):
        self.fs, path = url.rsplit("//",1)
        self.path = "/"+path
        super(DataSource, self).__init__(self.fs)
    
    def get_all_root_files(self, rel_url, files = []):
        status, listing = self.dirlist(self.path+rel_url, DirListFlags.STAT)
        for entry in listing:
            if entry.statinfo.flags == 19: # is a folder
                self.get_all_root_files(rel_url+"/"+entry.name, files)    
            elif ".root" in entry.name:
                files.append(rel_url+"/"+entry.name)
        return files

    def copy_all_root_files(self, rel_url, dest, test_run = False):
        files = natural_sort(self.get_all_root_files(rel_url, []))
        cp = client.CopyProcess()  
        for i,r_file in enumerate(files):
            remote = self.fs + "/" + self.path + "/" + r_file
            local = dest + "/" + "tree_{}.root".format(i) 
            if test_run:
                print("copy {0} to {1}".format(remote, local)) 
            else:    
                cp.add_job(remote, local)
        cp.prepare()
        cp.run()


