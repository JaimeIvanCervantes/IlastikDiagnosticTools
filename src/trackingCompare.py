import csv
import matplotlib.pyplot as plt
import numpy as np
import argparse
import sys


def main(parsedArgs):
    # Get data from both csv files
    dataPgmlink = np.genfromtxt(parsedArgs.file_pgmlink, dtype=float, delimiter=',', names=True)
    dataHytra = np.genfromtxt(parsedArgs.file_hytra, dtype=float, delimiter=',', names=True)
    
    
    objNumPgmlink = []
    objNumHytra = []
    
    mergerNumPgmlink = []
    mergerNumHytra = []
    
    countPgmlink = []
    countHytra = []
    
    # Get number of objects and mergers per frame for pgmlink data
    prevTimestep = None
    for index, timestep in enumerate(dataPgmlink['timestep']):
        idPgmlink = dataPgmlink['lineage_id'][index]
        
        if timestep == prevTimestep:
            if idPgmlink:
                objNumPgmlink[-1] += 1
            else:
                mergerNumPgmlink[-1] += 1
        else:
            objNumPgmlink.append(0)
            mergerNumPgmlink.append(0)
            
        prevTimestep = timestep

    # Get number of objects and mergers per frame for hytra data 
    prevTimestep = None
    for index, timestep in enumerate(dataHytra['timestep']):
        idHytra = dataHytra['lineage_id'][index]
        
        if timestep == prevTimestep:
            if idHytra:
                objNumHytra[-1] += 1
            else:
                mergerNumHytra[-1] += 1
        else:
            objNumHytra.append(0)
            mergerNumHytra.append(0) 
            
        prevTimestep = timestep
    
    # Check that size of arrays is equal
    assert len(objNumPgmlink) == len(objNumHytra), "Error: Length of hytra and pgmlink object arrays must be equal."
    assert len(mergerNumPgmlink) == len(mergerNumHytra), "Error: Length of hytra and pgmlink merger arrays must be equal."
    
    # Get diff between number of objects for pgmlink and hytra
    objNumDiff = np.array(objNumPgmlink) - np.array(objNumHytra)
    mergerNumDiff = np.array(mergerNumPgmlink) - np.array(mergerNumHytra)
            
    plt.plot(mergerNumDiff)
    plt.show()
    
               

if __name__ == "__main__":
     
    parser = argparse.ArgumentParser( description="Compare csv tracking files." )
    
    parser.add_argument('--file-pgmlink', help='Name of csv file 1', default='pgmlink.csv')
    parser.add_argument('--file-hytra', help='Name of csv file 2', default='hytra.csv')
     
    parsedArgs, workflowCmdlineArgs = parser.parse_known_args()
    
    parsedArgs.file_pgmlink = '/groups/branson/home/cervantesj/profiling/Alice/Fly_Bowl/data/GMR_71G01_AE_01_TrpA_Rig2Plate14BowlC_20110707T154934/movie5000-exported_data_table_pgmlink.csv'
    parsedArgs.file_hytra = '/groups/branson/home/cervantesj/profiling/Alice/Fly_Bowl/data/GMR_71G01_AE_01_TrpA_Rig2Plate14BowlC_20110707T154934/movie5000-exported_data_table_hytra.csv'
    
    main(parsedArgs) 