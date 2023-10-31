#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pandas as pd
from hashlib import sha256
from matplotlib import font_manager
from compress_pickle import dump, load


def makeFolder(path):
    """Crates a folder in the specified directory.

    Args:
        path (string): Path of the folder than needs to be created.

    """
    if not os.path.exists(path):
        try:
            os.mkdir(path)
        except OSError:
            raise OSError(
                    "Can't create destination directory (%s)!" % (path)
                )
            
def isNotebook():
    """Checks if the script is running from a Jupyter environment.

    Returns:
        bool: Flags Jupyter environment. 
    """
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False    

def getFontFile(family, weight='regular'):
    font = font_manager.FontProperties(family=family, weight=weight)
    file = font_manager.findfont(font)
    return file

def hashFilename(string, length=20):
    # https://stackoverflow.com/questions/14023350/cheap-mapping-of-string-to-small-fixed-length-string
    string = string.encode('utf-8')
    if length<len(sha256(string).hexdigest()):
        return sha256(string).hexdigest()[:length].upper()
    else:
        x = str(len(sha256(string).hexdigest()))
        exStr = f"Length too long. Length of {length} when hash length is {x}."
        raise Exception(exStr)

def loadDatabase(DBPath, df=True):
    exists = os.path.isfile(DBPath)
    if df:
        db = load(DBPath) if exists else pd.DataFrame()
    else:
        db = load(DBPath) if exists else dict()
    return db
        
def dumpDatabase(database, DBPath):
    dump(database, DBPath)
    return True

def exportDatabase(database, DBPath):
    database.to_csv(DBPath, index=False)
    
    
def listPalToStr(listPal):
    return str(listPal).replace('[','').replace(']','').replace("'",'')