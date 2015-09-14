import h5py
import numpy as np
import matplotlib.pylab as plt
import os
import time
import csv
import StringIO
import subprocess
import argparse

#from feature_selection import get_features_to_remove
from FeatureParser import FeatureParser
from ProjectFileOps import ProjectFileOps
from Report import Report

FEATURE_NUM = 4 #37
TREE_NUM = 30 # Number of trees for feature test
TREE_RANGE = range(1,50) # Range of trees for trees test  

# Features removal test
def main(parsedArgs) :
    featureToRemove = []
    
    projectFileOps = ProjectFileOps()
    featureParser = FeatureParser()

    # Paths 
    runCommand = parsedArgs.run_command
    path = os.path.dirname(parsedArgs.project_file)
    dataFile =  parsedArgs.data_file
    projectFile = parsedArgs.project_file
    bufferProjectFile = os.path.join(path, 'buffer.ilp') 
    dateId = time.strftime('%M%H%d%m%y')
    outFeaturesFile = os.path.join(path, dateId+'_{nickname}_')
    outTreesFile = os.path.join(path, dateId+'_{nickname}_')
    logFeaturesFile = os.path.join(path, dateId+'_features.log')
    logTreesFile = os.path.join(path, dateId+'_trees.log')
   
    # Run feature removal test test
    if parsedArgs.features_test :        
        
        # Loop through each feature in matrix        
        for fti in range(FEATURE_NUM) : #range(0, len(features_to_remove)-1) :
               
            if os.path.isfile(os.path.join(path,'varimp.txt')) and fti > 0 :
            #if len(features_to_remove) > 0 :
                #features_matrix_data[features_to_remove[0][1]] = False

                features = featureParser.getFeatures(os.path.join(path,'varimp.txt')) 
                
                featureToRemove.append(features[0][1]) #features_to_remove[0][1]) 
                #ftindices.append(features[0][1]) #features_to_remove[0][1])   
                #print "Indices: ", ftindices

            # Copy project file to buffer project file with removed features           
            projectFileOps.copyFileWithFeaturesRemoved(projectFile, bufferProjectFile, featureToRemove)#ftindices)
         
            # Get feature ID
            if len(str(fti)) == 1 :
                featureId = '0' + str(fti) 
            else :
                featureId = str(fti)
            
	    # Run command            
            command = runCommand +\
            ' --headless' +\
            ' --tree-count='+str(TREE_NUM) +\
            ' --retrain' +\
            ' --variable-importance-path='+path +\
            ' --export_source=\"Simple Segmentation\"' +\
            ' --output_filename_format='+outFeaturesFile+featureId+'_features_segmentation.h5' +\
            ' --project='+bufferProjectFile +\
            ' '+dataFile+'/data' +\
            ' 2>&1 | tee -a '+logFeaturesFile 
            
            print command
        
            # Open OS process and wait
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            retval = process.wait() 
 
    # Tests with increasing trees
    if parsedArgs.trees_test :
        for tri in TREE_RANGE: #range(1,45,1) :
            
            if len(str(tri)) == 1 :
                treeId = '0' + str(tri) 
            else :
                treeId =  str(tri)    
            
            # Run command 
            command = runCommand +\
            ' --headless' +\
            ' --tree-count='+str(tri) +\
            ' --retrain' +\
            ' --export_source=\"Simple Segmentation\"' +\
            ' --output_filename_format='+outTreesFile+treeId+'_trees_segmentation.h5' +\
            ' --project='+projectFile +\
            ' '+dataFile+'/data' +\
            ' 2>&1 | tee -a '+logTreesFile 
            
            print command
            
            # Open OS process and wait
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)      
            retval = process.wait() 


    # Generate report
    featuresReport = Report(logFeaturesFile)
    featuresReport = Report(logTreesFile)

if __name__ == "__main__":

    parser = argparse.ArgumentParser( description="Export video to HDF5 format." )
    
    parser.add_argument('--run-command', help='Ilastik run command (default: ./run_ilastik.sh).', default='./run_ilastik.sh')
    parser.add_argument('--data-file', help='Name of HDF5 data file.', required=True)
    parser.add_argument('--project-file', help='Name of project file.', required=True)
    parser.add_argument('--trees-test', help='Enable increasing-trees test.', action='store_true', default=False)
    parser.add_argument('--features-test', help='Enable feature-removal test.', action='store_true', default=False)
    
    parsedArgs, workflowCmdlineArgs = parser.parse_known_args()
    
    main(parsedArgs)

