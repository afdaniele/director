'''
Created by:

@author: Andrea F Daniele - TTIC - Toyota Technological Institute at Chicago
Feb 6, 2019 - Mountain View, CA

'''

import sys
import numpy as np
from os.path import isfile

class ProgressBar(object):

  def __init__(self, maxVal=100, precision=5, doneMessage=True ):
    self.maxVal = float( max(1.0, maxVal) )
    self.doneMessage = doneMessage
    self.precision = precision
    self.currentLength = -1
    self.currentVal = 0.0
    self.barParts = [ '[0%' ]
    for i in range(10,101,10): self.barParts.extend( ['.'] * self.precision + ['%d%%' % i] )
    self.barParts[-1] += ']'
    if doneMessage: self.barParts[-1] += ' Done!'
    self.barLength = len(self.barParts)
    self.step = float(self.barLength-1) / self.maxVal

  def next(self):
    newLength = int(np.floor( (self.currentVal + 1.0) * self.step ))
    if newLength > self.currentLength and newLength <= self.barLength:
      for i in range(self.currentLength+1, newLength+1):
        sys.stdout.write(self.barParts[i]); sys.stdout.flush()
      if newLength == self.barLength-1: print
      self.currentLength = newLength
    self.currentVal += 1

  def setMessage(self, message):
    self.barParts[-1] = '100%%] :: %s\n' % message


class FileReader(object):

  def __init__(self, file_path):
    if not isfile(file_path):
      raise ValueError("The file '%s' does not exist" % file_path)
    self._file_path = file_path
    # open file
    self._lines = None

  def lines(self):
    # read lines
    if not self._lines:
      with open(self._file_path, "r") as fo:
        self._lines = fo.readlines()
    # return lines
    return self._lines
