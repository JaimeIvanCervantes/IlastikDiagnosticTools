###############################################################################
#   ilastik: interactive learning and segmentation toolkit
#
#       Copyright (C) 2011-2014, the ilastik developers
#                                <team@ilastik.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# In addition, as a special exception, the copyright holders of
# ilastik give you permission to combine ilastik with applets,
# workflows and plugins which are not covered under the GNU
# General Public License.
#
# See the LICENSE file for details. License information is also available
# on the ilastik web site at:
#                  http://ilastik.org/license.html
###############################################################################

import h5py
import numpy as np
import matplotlib.pylab as plt
import os
import time
import csv
import StringIO
import subprocess
import argparse
import sys

#from feature_selection import get_features_to_remove
from FeatureParser import FeatureParser
from ProjectFileOps import ProjectFileOps
from Report import Report

FEATURE_NUM = 4 #37 # Max number of features to remove
TREE_NUM = 30 # Number of trees for feature test
TREE_RANGE = range(1,50) # Range of trees for trees test  

# Features removal test
def main(parsedArgs) :
    featureToRemove = []
    
    projectFileOps = ProjectFileOps()
    featureParser = FeatureParser()

    runCommand = parsedArgs.run_command
    path = os.path.dirname(parsedArgs.project_file)
    projectFile = parsedArgs.project_file
    projectFileRemovedLane = os.path.join(path, 'projectWithRemovedLane.ilp') 
    projectFileRemovedFeatures = os.path.join(path, 'projectWithRemovedFeatures.ilp') 
    dateId = time.strftime('%M%H%d%m%y')
    outFeaturesFile = os.path.join(path, dateId+'_{nickname}_')
    outTreesFile = os.path.join(path, dateId+'_{nickname}_')
    logFeaturesFile = os.path.join(path, dateId+'_features.log')
    logTreesFile = os.path.join(path, dateId+'_trees.log')
   
    # Remove last lane (video from project file)
    dataFile = projectFileOps.removeLastLane(projectFile, projectFileRemovedLane)
   
    # Run feature removal test test
    if parsedArgs.features_test :        
        
        # Loop through each feature in matrix        
        for fti in range(FEATURE_NUM) : 
               
            if os.path.isfile(os.path.join(path,'varimp.txt')) and fti > 0 :
                features = featureParser.getFeaturesFromImportanceTable(os.path.join(path,'varimp.txt')) 
                
                # Append least importance feature for removing
                featureToRemove.append(features[0][1]) 

            # Copy project file to buffer project file with removed features           
            projectFileOps.copyFileWithFeaturesRemoved(projectFileRemovedLane, projectFileRemovedFeatures, featureToRemove)
         
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
            ' --project='+projectFileRemovedFeatures +\
            ' '+dataFile +\
            ' 2>&1 | tee -a '+logFeaturesFile 
            
            print command
        
            # Open OS process and wait
            #process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            #retval = process.wait() 
 
    # Tests with increasing trees
    if parsedArgs.trees_test :
        # Remove last lane (video from project file)
        dataFile = projectFileOps.removeLastLane(projectFile, projectFileRemovedLane)
        
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
            ' --project='+projectFileRemovedLane +\
            ' '+dataFile +\
            ' 2>&1 | tee -a '+logTreesFile 
            
            print command
            
            # Open OS process and wait
            #process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)      
            #retval = process.wait() 


    # Generate report
    featuresReport = Report(logFeaturesFile)
    treesReport = Report(logTreesFile)

if __name__ == "__main__":
    # Uncomment for debugging
    '''
    sys.argv.append('--run-command=/opt/local/miniconda/envs/ilastik-devel/run_ilastik.sh')
    sys.argv.append('--project-file=/groups/branson/home/cervantesj/profiling/test/larvaeRemovedVideo.ilp')
    '''
    
    parser = argparse.ArgumentParser( description="Export video to HDF5 format." )
    
    parser.add_argument('--run-command', help='Ilastik run command (default: ./run_ilastik.sh).', default='./run_ilastik.sh')
    parser.add_argument('--project-file', help='Name of project file.', required=True)
    parser.add_argument('--trees-test', help='Enable increasing-trees test.', action='store_true', default=True)
    parser.add_argument('--features-test', help='Enable feature-removal test.', action='store_true', default=True)
    
    parsedArgs, workflowCmdlineArgs = parser.parse_known_args()
    
    main(parsedArgs)

