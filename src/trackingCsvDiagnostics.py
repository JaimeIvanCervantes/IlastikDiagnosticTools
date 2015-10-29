import csv
from pylab import *
import numpy as np
import argparse
import sys

class TrackingDiagnostics:
    def __init__(self, fileName): 
        self.data = np.genfromtxt(fileName, dtype=float, delimiter=',', names=True)
        
        self.objectNum = np.array([])
        self.errorStatus = np.array([])
        self.collisionNum = np.array([])
        
        prevTimestep = None

        prevLineageIds = []
        lineageIds = []
        
        for index, timestep in enumerate(self.data['timestep']):

            if timestep == prevTimestep:
                if self.data['lineage_id'][index] != 0:
                    self.objectNum[-1] += 1
                
                lineageIds.append(self.data['lineage_id'][index])
            else:    
                self.objectNum = np.append(self.objectNum,1)
                
                status = 0 
                
                for lineageId in lineageIds:
                    if prevLineageIds and lineageId != 0.0 and lineageId not in prevLineageIds:
                        print "new ID found. Frame: {}, ID: {}".format(timestep, lineageId)
                        status = 1
                    if prevLineageIds and lineageId != 0.0 and lineageIds.count(lineageId) > 1:
                        print "ID repeated in Frame: {}, ID: {}".format(timestep,lineageId)
                        status = 2
                    
                self.collisionNum= np.append(self.collisionNum, (lineageIds.count(0)))
                                      
                prevLineageIds = lineageIds 
                lineageIds = [self.data['lineage_id'][index]] 
                
                self.errorStatus = np.append(self.errorStatus,status)
                               
            prevTimestep = timestep
        
    def plotLineageIds(self):

        plot(self.data['timestep'], self.data['lineage_id'], linestyle='None', marker='o', markersize=10)
        ylim([-1,25])
        title('Lineage IDs vs Frame Number')
        ylabel('Lineage IDs')
        xlabel('Frame Number')
        show()

    def plotObjectNum(self):
        plot(self.objectNum, linestyle='--', marker='o', markeredgecolor='b', color='r')
        title('Object Number vs Frame Number')
        ylabel('Object Number')
        xlabel('Frame Number')
        show()
    
    def plotErrors(self):
        figure()
        plot(self.errorStatus, linestyle='None', marker='o')
        show()
      
    def plotBoundingRect(self, frame):
        figure()
        currentAxis = gca()

        pos = self.data['timestep'] == frame

        x = self.data['CoordMinimum_0'][pos]
        y = self.data['CoordMinimum_1'][pos] 
        
        width = self.data['CoordMaximum_0'][pos] - self.data['CoordMinimum_0'][pos]
        height = self.data['CoordMaximum_1'][pos] - self.data['CoordMinimum_1'][pos] 

        lineageIds = self.data['lineage_id'][pos]

        for index in range(len(x)):
            if lineageIds[index] == 0:
                currentAxis.add_patch(Rectangle((x[index], y[index]), width[index], height[index], fill=None, alpha=1, color='r'))
            else:
                currentAxis.add_patch(Rectangle((x[index], y[index]), width[index], height[index], fill=None, alpha=1, color='b'))

        maxX = np.max(self.data['CoordMaximum_0'][pos])
        maxY = np.max(self.data['CoordMaximum_1'][pos])  
        xlim([0,maxX])
        ylim([0,maxY])
        
        currentAxis.invert_yaxis()
        show()
    
    def plotCollisions(self):
        figure()
        plot(self.collisionNum, linestyle='--', marker='o', markersize=10, markeredgecolor='b', color='r')    
        title('Collision Number')
        ylabel('Collision Number')
        xlabel('Frame Number')
        show()    
        
    def plotTracks(self):
        figure()
        
        lineageIds = np.unique(self.data['lineage_id'])
        lineageIds = np.delete(lineageIds, 0 )
        
        for lineageId in lineageIds:
            plot(self.data['RegionCenter_0'][self.data['lineage_id']==lineageId], self.data['RegionCenter_1'][self.data['lineage_id']==lineageId], color=np.random.rand(3,))
        show()

def main(parsedArgs):
    diagnostics = TrackingDiagnostics(parsedArgs.file) 
    
    if parsedArgs.lineageIds:
        diagnostics.plotLineageIds()
    if parsedArgs.tracks: 
        diagnostics.plotTracks()
    if parsedArgs.objectNum: 
        diagnostics.plotObjectNum()
    if parsedArgs.errors: 
        diagnostics.plotErrors()
    if parsedArgs.collisions:
        diagnostics.plotCollisions()
    if parsedArgs.boundingRect:
        diagnostics.plotBoundingRect(parsedArgs.boundingRect)

   
if __name__ == "__main__":
     
    parser = argparse.ArgumentParser( description="Export video to HDF5 format." )
    
    parser.add_argument('--file', help='Name of conservation-tracking csv file.', default='../data/GMR_71G01_AE_01_TrpA_Rig2Plate14BowlC_20110707T154934-exported_data_table.csv')
    parser.add_argument('--lineage-ids',  help='Plot the lineage IDs.', dest='lineageIds', action='store_true', default=False)
    parser.add_argument('--tracks', help='Plot the tracks of all the objects in the file', dest='tracks', action='store_true', default=False)
    parser.add_argument('--object-num', help='Plot the number of objects per frame', dest='objectNum', action='store_true', default=False)
    parser.add_argument('--errors', help='Plot the errors per frame. These errors include appearing IDs and repeated IDs', dest='errors', action='store_true', default=False)
    parser.add_argument('--collisions', help='Plot the number of collisions per frame.', dest='collisions', action='store_true', default=False)
    parser.add_argument('--bounding-rect', help='Plot the bounding rectangles for the choose frame.', dest='boundingRect', default=None, type=int)
     
    parsedArgs, workflowCmdlineArgs = parser.parse_known_args()
    
    main(parsedArgs) 




