#----------------------------------------------------------------------
# $Id: read_lund_json.py 1157 2018-08-22 20:11:52Z frdreyer $
#
# Copyright (c) -, Frederic A. Dreyer, Gavin P. Salam, Gregory Soyez
#
#----------------------------------------------------------------------
# This file is part of FastJet contrib.
#
# It is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
#
# It is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
# License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this code. If not, see <http://www.gnu.org/licenses/>.
#----------------------------------------------------------------------

from abc import ABC, abstractmethod
import numpy as np
from math import log, ceil, cos, sin
import json, gzip, sys

#----------------------------------------------------------------------
class Reader(object):
    """
    Reader for files consisting of a sequence of json objects, one per line
    Any pure string object is considered to be part of a header (even if it appears at the end!)
    """
    def __init__(self, infile, nmax = -1):
        self.infile = infile
        self.nmax = nmax
        self.reset()

    def set_nmax(self, nmax):
        self.nmax = nmax

    def reset(self):
        """
        Reset the reader to the start of the file, clear the header and event count.
        """
        if self.infile.endswith('.gz'):
            self.stream = gzip.open(self.infile,'r')
        else:
            self.stream = open(self.infile,'r')
        self.n = 0
        self.header = []
        
        
    #----------------------------------------------------------------------
    def __iter__(self):
        # needed for iteration to work 
        return self
        
    def __next__(self):
        ev = self.next_event()
        if (ev is None): raise StopIteration
        else           : return ev

    def next(self): return self.__next__()
        
    def next_event(self):

        # we have hit the maximum number of events
        if (self.n == self.nmax):
            #print ("# Exiting after having read nmax jet declusterings")
            return None
        
        try:
            line = self.stream.readline()
            if self.infile.endswith('.gz'):
                j = json.loads(line.decode('utf-8'))
            else:
                j = json.loads(line)
        except IOError:
            print("# got to end with IOError (maybe gzip structure broken?) around event", self.n, file=sys.stderr)
            return None
        except EOFError:
            print("# got to end with EOFError (maybe gzip structure broken?) around event", self.n, file=sys.stderr)
            return None
        except ValueError:
            print("# got to end with ValueError (empty json entry?) around event", self.n, file=sys.stderr)
            return None

        # skip this
        if (type(j) is str):
            self.header.append(j)
            return self.next_event()
        self.n += 1
        return j

#------------------------------------------------------------------    
class Image(ABC):
    """Image which transforms point-like information into pixelated 2D
    images which can be processed by convolutional neural networks."""
    def __init__(self, infile, nmax=-1):
        if (type(infile) is Reader): 
            self.reader = infile
            self.reader.set_nmax(nmax)
        else:                        
            self.reader = Reader(infile, nmax)

    @abstractmethod
    def process(self, event):
        pass
    
    def values(self):
        res = []
        while True:
            event = self.reader.next_event()
            if event!=None:
                res.append(self.process(event))
            else:
                break
        self.reader.reset()
        return res

        
        
class LundImage(Image):
    """
    Take input file and transforms it into parsable lund image.
    """
    def __init__(self, infile, nmax, npxl, xval = [0.0, 7.0], yval = [-3.0, 7.0]):
        Image.__init__(self, infile, nmax)
        self.npxl = npxl
        self.xmin = xval[0]
        self.ymin = yval[0]
        self.x_pxl_wdth = (xval[1] - xval[0])/npxl
        self.y_pxl_wdth = (yval[1] - yval[0])/npxl

    def process(self, event):
        res = np.zeros((self.npxl,self.npxl))
        L1norm = 0.0

        for declust in event:
            x = log(1.0/declust['Delta'])
            y = self.ptcoord(declust)
            psi = declust['psi']
            xind = ceil((x - self.xmin)/self.x_pxl_wdth - 1.0)
            yind = ceil((y - self.ymin)/self.y_pxl_wdth - 1.0)
            # print((x - self.xmin)/self.x_pxl_wdth,xind,
            #       (y - self.ymin)/self.y_pxl_wdth,yind,':',
            #       declust['delta_R'],declust['pt2'])
            if (max(xind,yind) < self.npxl and min(xind, yind) >= 0):
                res[xind,yind] += 1
                L1norm += 1.0
        if L1norm > 0.0:
            res = res/L1norm
        return res
    
    def ptcoord(self, declust):
        val = declust['kt']
        return log(val)
    

class LundDense(Image):
    """
    Take input file and transforms it into parsable lund sequence.
    """
    def __init__(self,infile, nmax, nlen, secondary=False):
        Image.__init__(self, infile, nmax)
        self.nlen      = nlen
        self.secondary = secondary
        
    def process(self, event):
        res = np.zeros((self.nlen if not self.secondary else self.nlen*2, 2))

        if self.secondary:
            event_secondary = event[1]
            event = event[0]
            for i in range(self.nlen):
                if (i>= len(event_secondary)):
                    break
                dec=self.fill_declust(event_secondary[i])
                res[self.nlen+i,:] = dec
                
        for i in range(self.nlen):
            if (i >= len(event)):
                break
            res[i,:] = self.fill_declust(event[i])
            
        return res

    def fill_declust(self,declust):
        res = np.zeros(2)
        res[0] = log(1.0/declust['Delta'])
        res[1] = self.ptcoord(declust)
        return res
        
    def ptcoord(self, declust):
        val = declust['kt']
        return log(val)
    
