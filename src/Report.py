import h5py
import numpy as np
from pylab import *
import os
import re
import string
import csv

# Generate plots and stats
class Report():
    def __init__(self, logFileName):
        self._logFileName = logFileName
        
    def showTimePlot(self):
        totalTimes = [] 
        
        # Get running time stats from log file
        with open(self._logFileName, 'r') as logFile:
                for line in logFile:
                    if re.search('execution took,', line):
                        list = line.split(',')
                        time = float(list[-1].strip())
                        totalTimes.append(time)
                        
        title('Test Running-Times')
        xlabel('Test Number')
        ylabel('Time Seconds (seconds)')
        
        plot(totalTimes)
        show()
        
    def showErrorPlot(self):
        pass
    
#report = Report('/groups/branson/home/cervantesj/profiling/Alice/Courtship_Bowls/3917100915_trees.log')
#report.showTimePlot()