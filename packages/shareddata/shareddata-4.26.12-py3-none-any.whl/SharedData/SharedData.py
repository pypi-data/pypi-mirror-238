import os
import psutil
import pandas as pd
import numpy as np
from multiprocessing import shared_memory
from pathlib import Path
from importlib.metadata import version
import warnings
import time
# Ignore the "invalid value encountered in cast" warning
warnings.filterwarnings("ignore", category=RuntimeWarning)

import SharedData.Defaults as Defaults
from SharedData.Logger import Logger
from SharedData.TableMemory import TableMemory
from SharedData.TableDisk import TableDisk
from SharedData.TimeseriesContainer import TimeseriesContainer
from SharedData.TimeSeries import TimeSeries
from SharedData.DataFrame import SharedDataFrame
from SharedData.AWSS3 import S3ListFolder
from SharedData.Utils import remove_shm_from_resource_tracker, cpp


class SharedData:
    

    def __init__(self, source, user='guest'):
        self.source = source
        self.user = user

        # DATA DICTIONARY
        self.data = {}

        # MEMORY MANAGEMENT
        self.memmaps = []

        # LOGIN VARIABLES
        self.islogged = False
        self.source = source
        self.user = user
        self.mode = 'rw'

        # S3 VARIABLES
        self.s3read = True
        self.s3write = True

        # save files locally
        self.save_local = (os.environ['SAVE_LOCAL'] == 'True')

        self.databases = {
            'MarketData':    ['date', 'symbol'],
            'Relationships': ['date', 'symbol', 'symbol1'],
            'Portfolios':    ['date', 'portfolio'],
            'Signals':       ['date', 'portfolio', 'symbol'],
            'Risk':          ['date', 'portfolio', 'symbol'],
            'Positions':     ['date', 'portfolio', 'symbol'],
            'Orders':        ['date', 'portfolio', 'symbol', 'clordid'],
            'Trades':        ['date', 'portfolio', 'symbol', 'tradeid']
        }

        Logger.connect(self.source, self.user)

        if (os.name == 'posix'):
            remove_shm_from_resource_tracker()

        if not self.islogged:
            self.islogged = True
            try:
                Logger.log.debug('User:%s,SharedData:%s CONNECTED!' %
                                 (self.user, version('SharedData')))
            except:
                Logger.log.debug('User:%s CONNECTED!' % (self.user))

        # [self.shm_mutex, self.globalmutex, self.ismalloc] = \
        #     self.mutex('SharedData', os.getpid())
        
        

    ###############################################
    ############# DATA CONTAINERS #################
    ###############################################
    
    ############# TABLE #################
    def table(self, database, period, source, tablename,
            names=None, formats=None, size=None, hasindex=True,\
            value=None, user='master', overwrite=False,\
            type='DISK', partitioning=None):

        path = user+'/'+database+'/'+period+'/'+source+'/table/'+tablename
        if not path in self.data.keys():
            if type == 'MEMORY':
                self.data[path] = TableMemory(self, database, period, source,
                                        tablename, records=value, names=names, formats=formats, size=size, hasindex=hasindex,
                                        user=user, overwrite=overwrite)
            elif type == 'DISK':
                self.data[path] = TableDisk(self, database, period, source,
                                        tablename, records=value, names=names, formats=formats, size=size, hasindex=hasindex,
                                        user=user, overwrite=overwrite, partitioning=partitioning)
        return self.data[path].records

    ############# TIMESERIES #################
    def timeseries(self, database, period, source, tag=None,
                   startDate=None, columns=None, value=None, user='master'):

        path = user+'/'+database+'/'+period+'/'+source+'/timeseries'
        if not path in self.data.keys():
            self.data[path] = TimeseriesContainer(
                self, database, period, source, user=user)
        if tag is None:
            return self.data[path]

        if not tag in self.data[path].tags.keys():
            if (startDate is None) & (columns is None) & (value is None):
                self.data[path].load()
                if not tag in self.data[path].tags.keys():
                    Logger.log.error('Tag %s/%s doesnt exist' % (path, tag))
                    return None
            else:
                self.data[path].tags[tag] = TimeSeries(self, self.data[path],
                                                       database, period, source, tag,
                                                       value=value, startDate=startDate, columns=columns, user=user)

        return self.data[path].tags[tag].data

    ############# DATAFRAME #################
    def dataframe(self, database, period, source,
                  date=None, value=None, user='master'):
        pass

    ###############################################
    ######### SHARED MEMORY MANAGEMENT ############
    ###############################################    

    @staticmethod
    def mutex(shm_name, pid):        
        dtype_mutex = np.dtype({'names': ['pid', 'type', 'isloaded'],\
                                'formats': ['<i8', '<i8', '<i8']})
        try:
            shm_mutex = shared_memory.SharedMemory(
                name=shm_name + '#mutex', create=True, size=dtype_mutex.itemsize)
            ismalloc = False
        except:                                            
            shm_mutex = shared_memory.SharedMemory(
                name=shm_name + '#mutex', create=False)
            ismalloc = True        
        mutex = np.ndarray((1,), dtype=dtype_mutex,buffer=shm_mutex.buf)[0]        
        SharedData.acquire(mutex, pid, shm_name)        
        # register process id access to memory
        fpath = Path(os.environ['DATABASE_FOLDER'])
        fpath = fpath/('shm/'+shm_name.replace('\\', '/')+'#mutex.csv')
        os.makedirs(fpath.parent, exist_ok=True)
        with open(fpath, "a+") as f:
            f.write(str(pid)+',')
        return [shm_mutex, mutex, ismalloc]
    
    @staticmethod
    def acquire(mutex, pid, relpath):
        tini = time.time()
        # semaphore is process safe
        telapsed = 0
        hdrptr = mutex.__array_interface__['data'][0]
        semseek = 0
        firstcheck = True
        while cpp.long_compare_and_swap(hdrptr, semseek, 0, pid) == 0:
            # check if process that locked the mutex is still running
            telapsed = time.time() - tini
            if (telapsed > 15) | ((firstcheck) & (telapsed > 1)):
                lockingpid = mutex['pid']
                if not psutil.pid_exists(lockingpid):
                    if cpp.long_compare_and_swap(hdrptr, semseek, lockingpid, pid) != 0:
                        break
                if not firstcheck:
                    Logger.log.warning('%s waiting for semaphore...' % (relpath))
                tini = time.time()
                firstcheck = False
            time.sleep(0.000001)

    @staticmethod
    def release(mutex, pid, relpath):
        hdrptr = mutex.__array_interface__['data'][0]
        semseek = 0
        if cpp.long_compare_and_swap(hdrptr, semseek, pid, 0) != 1:
            Logger.log.error(
                '%s Tried to release semaphore without acquire!' % (relpath))
            raise Exception('Tried to release semaphore without acquire!')

    # TODO: check free memory before allocate    
    @staticmethod
    def malloc(shm_name, create=False, size=None):
        ismalloc = False
        shm = None
        if not create:
            try:
                shm = shared_memory.SharedMemory(
                    name=shm_name, create=False)
                ismalloc = True
            except:
                pass            
        elif (create) & (not size is None):
            try:
                shm = shared_memory.SharedMemory(
                    name=shm_name, create=True, size=size)                
                ismalloc = False
            except:                                            
                shm = shared_memory.SharedMemory(
                    name=shm_name, create=False)
                ismalloc = True
                
        elif (create) & (size is None):
            raise Exception(
                'SharedData malloc must have a size when create=True')
        
        # register process id access to memory
        fpath = Path(os.environ['DATABASE_FOLDER'])
        fpath = fpath/('shm/'+shm_name.replace('\\', '/')+'.csv')
        os.makedirs(fpath.parent, exist_ok=True)
        pid = os.getpid()
        with open(fpath, "a+") as f:
            f.write(str(pid)+',')

        return [shm, ismalloc]

    @staticmethod
    def free(shm_name):
        if os.name == 'posix':
            try:
                shm = shared_memory.SharedMemory(
                    name=shm_name, create=False)
                shm.close()
                shm.unlink()
                fpath = Path(os.environ['DATABASE_FOLDER'])
                fpath = fpath/('shm/'+shm_name.replace('\\', '/')+'.csv')
                if fpath.is_file():
                    os.remove(fpath)
            except:
                pass

    @staticmethod
    def freeall():
        shm_names = SharedData.list_memory()
        for shm_name in shm_names.index:
            SharedData.free(shm_name)

    @staticmethod
    def list_memory():
        folder = Path(os.environ['DATABASE_FOLDER'])/'shm'
        shm_names = pd.DataFrame()
        for root, _, filepaths in os.walk(folder):
            for filepath in filepaths:
                if filepath.endswith('.csv'):
                    fpath = os.path.join(root, filepath)
                    shm_name = fpath.removeprefix(str(folder))[1:]
                    shm_name = shm_name.removesuffix('.csv')
                    shm_name = shm_name.replace('/', '\\')
                    try:
                        shm = shared_memory.SharedMemory(
                            name=shm_name, create=False)
                        shm_names.loc[shm_name, 'size'] = shm.size
                        shm.close()
                    except:
                        try:
                            if fpath.is_file():
                                os.remove(fpath)
                        except:
                            pass
        shm_names = shm_names.sort_index()
        return shm_names

    ######### LIST ############
    @staticmethod
    def list(keyword, user='master'):
        mdprefix = user+'/'
        keys = S3ListFolder(mdprefix+keyword)
        keys = keys[['.bin' in k for k in keys]]
        keys = [k.replace(mdprefix, '').split('.')[0]
                .replace('/head', '').replace('/tail', '')\
                .replace('_head', '').replace('_tail', '')
                for k in keys]
        keys = np.unique(keys).tolist()
        return keys
