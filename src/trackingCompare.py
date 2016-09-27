import matplotlib.pyplot as plt
import numpy as np
import argparse
from sklearn.utils.linear_assignment_ import linear_assignment
    
class TrackingComparison():
    
    def __init__(self, filePgmlink, fileHytra):
        # Get data from both csv files
        self.dataPgmlink = np.genfromtxt(parsedArgs.filePgmlink, dtype=float, delimiter=',', names=True)
        self.dataHytra = np.genfromtxt(parsedArgs.fileHytra, dtype=float, delimiter=',', names=True)
    
    def getObjectNumDiff(self):  
        """
        Get comparison for the difference in number of objects and number of mergers.
        """  
        objNumPgmlink = []
        objNumHytra = []
         
        mergerNumPgmlink = []
        mergerNumHytra = []
         
        # Get number of objects and mergers per frame for pgmlink data   
        prevTime = None
        for i, time in enumerate(self.dataPgmlink['timestep']):
            idPgmlink = self.dataPgmlink['lineage_id'][i]
             
            if time == prevTime:
                if idPgmlink == 0:
                    if mergerNumPgmlink:
                        mergerNumPgmlink[-1] += 1
                    else:
                        mergerNumPgmlink.append(1)
                else:
                    if objNumPgmlink:
                        objNumPgmlink[-1] += 1
                    else:
                        objNumPgmlink.append(1)
            else:
                mergerNumPgmlink.append(1)
                objNumPgmlink.append(1)
                           
            prevTime = time
     
        # Get number of objects and mergers per frame for hytra data 
        print 'Getting object num for hytra'
         
        prevTime = None
        for i, time in enumerate(self.dataHytra['timestep']):
            idHytra = self.dataHytra['lineage_id'][i]
             
            if time == prevTime:
                if idHytra == 0:
                    if mergerNumHytra:
                        mergerNumHytra[-1] += 1
                    else:
                        mergerNumHytra.append(1)
                else:
                    if objNumHytra:
                        objNumHytra[-1] += 1
                    else:
                        objNumHytra.append(1)
            else:
                mergerNumHytra.append(1)
                objNumHytra.append(1)
                                 
            prevTime = time
     
        # Check that size of arrays is equal
        assert len(objNumPgmlink) == len(objNumHytra), "Error: Length of hytra and pgmlink object arrays must be equal."
        assert len(mergerNumPgmlink) == len(mergerNumHytra), "Error: Length of hytra and pgmlink merger arrays must be equal."
         
        # Get diff between number of objects for pgmlink and hytra
        objNumDiff = np.array(objNumPgmlink) - np.array(objNumHytra)
        mergerNumDiff = np.array(mergerNumPgmlink) - np.array(mergerNumHytra)
        
        # Plots
        plt.figure(1)
        
        plt.subplot(211) 
        plt.title('Object Number Diff per Frame')
        plt.xlabel('Frame Number')        
        plt.ylabel('Object Num Diff')
        plt.plot(objNumDiff)

        plt.subplot(212) 
        plt.title('Merger Number Diff per Frame')
        plt.xlabel('Frame Number')        
        plt.ylabel('Object Num Diff')
        plt.plot(mergerNumDiff)
        plt.show() 


    def getIdMatchDiff(self):
        """
        Get comparison plots for the distance, area, an ID match differences between PgmLink and Hytra
        """
        
        # Compare tracking using the hungarian algorithm    
        disDiffPerFrame = []
        areaDiffPerFrame = []
        idsMismatchPerFrame = []
        
        newj = 0
        startj = 0
        
        prevTimePgmlink = 0
    
        idsPgmlink = []
        idsHytra = []
        
        distanceAndAreaDict = {}
        
        prevIdsMatch = None
        
        for i in range(len(self.dataPgmlink['timestep'])):
            idPgmlink = self.dataPgmlink['lineage_id'][i]
            
            # IDs 0 and 1 reserved for mergers and errors
            if idPgmlink < 2:
                continue
                    
            timePgmlink = self.dataPgmlink['timestep'][i]
            areaPgmlink = self.dataPgmlink['Count'][i]
            
            centerPgmlink = np.array([ self.dataPgmlink['RegionCenter_0'][i], self.dataPgmlink['RegionCenter_1'][i] ])
            
            # On new timestep match IDs
            if timePgmlink != prevTimePgmlink:                                            
                # Initialize square distance cost and area matrices (mssing IDs add a cost of 1000)
                missingIdCost = 1000.0
                idsPgmlink.sort()
                idsHytra.sort()
                maxLen = max(len(idsPgmlink), len(idsHytra))  
                distanceMat = np.full( (maxLen, maxLen), missingIdCost ) 
                areasMat = np.full( (maxLen, maxLen), 0.0 )                       
                
                # Populate distance matrix
                for (idp, idh), (distance, area) in distanceAndAreaDict.items():
                    indexPgmlink = idsPgmlink.index(idp)
                    indexHytra =  idsHytra.index(idh)
                    
                    distanceMat[indexPgmlink, indexHytra] = distance
                    areasMat[indexPgmlink, indexHytra] = area
     
                # Run hungarian algorithm to match IDs and minimize distance distanceMat
                result = linear_assignment(distanceMat)
                
                # Get total distance and area for result
                totalDistance = sum(distanceMat[cell[0]][cell[1]] for cell in result)
                totalArea = sum(areasMat[cell[0]][cell[1]] for cell in result)
                
                # Append results
                disDiffPerFrame.append(totalDistance)
                areaDiffPerFrame.append(totalArea)
                
                # Get ID match diff between frames
                if len(idsPgmlink) == len(idsHytra):
                    idsMatch = [(idsPgmlink[indp], idsHytra[indh]) for [indp, indh] in result] #map(tuple, result)
                    
                    # Increase idMismatchCount for each mismatch
                    if prevIdsMatch:
                        idMismatchCount = 0
                        for ids in idsMatch:
                            if ids not in prevIdsMatch:
                                idMismatchCount += 1
                                
                        idsMismatchPerFrame.append(idMismatchCount)
                     
                    prevIdsMatch = idsMatch
                else:
                    # Append -1 when Pgmlink and Hytra don't have the same number of IDs
                    idsMismatchPerFrame.append(-1)
                    
                # Set start of hytra loop
                startj = newj
                
                # Clear distance and area dicts
                idsPgmlink = []
                idsHytra = []
                distanceAndAreaDict = {}
            
            # Loop through hytra objects
            for j in range(startj, len(self.dataHytra['timestep'])):
                timeHytra = self.dataHytra['timestep'][j]
                
                # Exit loop when hytra's time exceeds pgmlink's time
                if timeHytra > timePgmlink:
                    newj = j
                    break              
                  
                idHytra = self.dataHytra['lineage_id'][j] 
                
                # IDs 0 and 1 reserved for mergers and errors
                if idHytra < 2:
                    continue
                            
                # Build ids list
                if idPgmlink not in idsPgmlink:
                    idsPgmlink.append(idPgmlink)
                
                if idHytra not in idsHytra:
                    idsHytra.append(idHytra)
                
                areaHytra = self.dataHytra['Count'][j]
                centerHytra = np.array([ self.dataHytra['RegionCenter_0'][j], self.dataHytra['RegionCenter_1'][j] ])
                
                # Add distance and area between object to dict
                distance = np.linalg.norm(centerPgmlink-centerHytra)
                area = areaPgmlink-areaHytra
                distanceAndAreaDict[(idPgmlink, idHytra)] = (distance, area) 
                
            # Store previous time step for PgmLink
            prevTimePgmlink = timePgmlink
        
        #Plots
        plt.figure(1)
        plt.subplot(311)   
        plt.title('Distance Diff per Frame')
        plt.xlabel('Frame Number')        
        plt.ylabel('Distance Cost (Pixels)')
        plt.plot(disDiffPerFrame)
     
        plt.subplot(312)
        plt.title('Area Diff per Frame')
        plt.xlabel('Frame Number')        
        plt.ylabel('Area Difference (Pixels)')
        plt.plot(areaDiffPerFrame)
        
        plt.subplot(313)
        plt.title('ID Mismatch')
        plt.xlabel('Frame Number')        
        plt.ylabel('Number ID Mismatches')
        plt.plot(idsMismatchPerFrame)
        plt.show() 


def main(parsedArgs):
    trackComp = TrackingComparison(parsedArgs.filePgmlink, parsedArgs.fileHytra) 
    
    if parsedArgs.idMatchDiff:
        trackComp.getIdMatchDiff()
    if parsedArgs.objectNumDiff: 
        trackComp.getObjectNumDiff()
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser( description="Compare csv tracking files." )
    
    parser.add_argument('--file-pgmlink', help='Name of csv file for Pgmlink', dest='filePgmlink', default='pgmlink.csv')
    parser.add_argument('--file-hytra', help='Name of csv file for Hytra', dest='fileHytra', default='hytra.csv')
    parser.add_argument('--id-match-diff',  help='Plot the distance and area difference.', dest='idMatchDiff', action='store_true', default=False)
    parser.add_argument('--object-num-diff',  help='Plot the number of objects difference.', dest='objectNumDiff', action='store_true', default=False)
     
    parsedArgs, workflowCmdlineArgs = parser.parse_known_args()
    
    # Uncomment for debugging
    parsedArgs.filePgmlink = '/groups/branson/home/cervantesj/profiling/Alice/Fly_Bowl/data/GMR_71G01_AE_01_TrpA_Rig2Plate14BowlC_20110707T154934/movie5000-exported_data_table_pgmlink.csv'
    parsedArgs.fileHytra = '/groups/branson/home/cervantesj/profiling/Alice/Fly_Bowl/data/GMR_71G01_AE_01_TrpA_Rig2Plate14BowlC_20110707T154934/movie5000-exported_data_table_hytra.csv'
    parsedArgs.idMatchDiff = True
    parsedArgs.objectNumDiff = False
    
    main(parsedArgs) 