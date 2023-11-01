import os
import threading
import time
import pandas as pd
import numpy as np
from pathlib import Path
from multiprocessing import shared_memory
import gzip
import io
import hashlib
from datetime import datetime
from tqdm import tqdm
import threading
import psutil

from SharedData.Logger import Logger
from SharedData.AWSS3 import S3Upload, S3Download, UpdateModTime, S3ListFolder
from SharedData.TableIndex import TableIndex
from SharedData.SharedNumpy import SharedNumpy
from SharedData.RealTime import RealTime
from SharedData.Table import Table

from SharedData.Utils import cpp


class TableDisk(Table):
    # TODO: create partitioning option yearly, monthly, daily

    def __init__(self, shareddata, database, period, source, tablename,
                 records=None, names=None, formats=None, size=None,hasindex=True,
                 overwrite=False, user='master', partitioning=None):
        self.type = 1
        self.shf_hdr = np.array([])
        self.shf_data = np.array([])
        super().__init__(shareddata, database, period, source, tablename,
                         records=records, names=names, formats=formats, size=size,hasindex=hasindex,
                         overwrite=overwrite, user=user, tabletype=self.type, partitioning=partitioning)

    ############### MALLOC ###############
    def malloc(self):     
        # create or extend currrent file
        self.create_file()
        
        # memory map header        
        self.shf_hdr = np.memmap(self.filepath,self.hdrdtype,'r+',0,(1,))
        self.shf_hdr[0] = self.hdr
        self.hdr = self.shf_hdr[0]
        self.hdr['recordssize'] = int(self.size)
        self.shf_hdr.flush()

        # memory map data
        offset = self.hdr.dtype.itemsize
        self.shf_data = np.memmap(self.filepath,self.recdtype,'r+',offset,(self.hdr['recordssize'],))
        self.records = SharedNumpy('DISK', self.shf_data)
        self.records.table = self
    

    ############### FREE ###############
    def free(self):        
        try:
            self.acquire()
            self.shf_hdr.flush()
            del self.shf_hdr
            self.shf_data.flush()
            del self.shf_data
            if self.hasindex:
                self.index.free()
            if self.relpath in self.shareddata.data:
                del self.shareddata.data[self.relpath]
            self.mutex['isloaded'] = 0
        except:
            pass
        finally:
            self.release()

    ############### WRITE ###############
    def write_file(self):
        # flush header
        self.shf_hdr.flush()
        # flush data
        self.shf_data.flush()
        # set the modify time of the file
        mtime = max(self.hdr['mtime'],
                    self.hdr['mtimehead'], self.hdr['mtimetail'])
        self.hdr['mtime'] = mtime
        os.utime(self.filepath, (mtime, mtime))
        # flush index
        if self.hdr['hasindex']==1:
            self.index.flush()
