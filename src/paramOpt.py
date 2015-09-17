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

CORRELATED_FEATURES = { "LG(0.7)" : (1,1), \
                  "LG(1.0)" : (1,2), \
                  "LG(1.6)" : (1,3), \
                  "LG(3.5)" : (1,4), \
                  "LG(5.0)" : (1,5), \
                  "LG(10.0)" : (1,6) } 

#from feature_selection import get_features_to_remove
from FeatureParser import FeatureParser
from ProjectFileOps import ProjectFileOps
from Report import Report

MAX_FEATURE_NUM = 37 # Max number of features to remove
TREE_NUM = 30 # Number of trees for feature test
TREE_RANGE = range(1,50) # Range of trees for trees test  

# Features removal test
def main(parsedArgs) :
    projectFileOps = ProjectFileOps()
    featureParser = FeatureParser()

    path = os.path.dirname(parsedArgs.project_file)
    if path == '':
        path='./'

    runCommand = parsedArgs.run_command
    projectFile = parsedArgs.project_file
    projectFileRemovedLane = os.path.join(path, 'projectWithRemovedLane.ilp') 
    projectFileRemovedFeatures = os.path.join(path, 'projectWithRemovedFeatures.ilp') 
    dateId = time.strftime('%M%H%d%m%y')
    outFeaturesFile = os.path.join(path, dateId+'_{nickname}_')
    outTreesFile = os.path.join(path, dateId+'_{nickname}_')
    logFeaturesFile = os.path.join(path, dateId+'_features.log')
    logTreesFile = os.path.join(path, dateId+'_trees.log')
   
    # Check that the script is being run from the same directory as the project file
    #assert os.getcwd() == path
   
    # Remove last lane (video from project file)
    dataFile = projectFileOps.removeLastLane(projectFile, projectFileRemovedLane)
   
    # Run feature removal test
    if parsedArgs.features_test :       
        featuresToRemove = []
        
        # Add highly correlated features to featuresToRemove
        for value in CORRELATED_FEATURES.itervalues():
            featuresToRemove.append(value)        
        
        count = 0
        while len(featuresToRemove) <= MAX_FEATURE_NUM and count < MAX_FEATURE_NUM:
        #for fti in range(FEATURE_NUM):   
            count += 1
            if os.path.isfile(os.path.join(path,'varimp.txt')) and count > 1 :
                features = featureParser.getFeaturesFromImportanceTable(os.path.join(path,'varimp.txt')) 
                
                # Append least importance feature for removing
                if features[0][1] not in featuresToRemove:
                    featuresToRemove.append(features[0][1]) 

            # Copy project file to buffer project file with removed features           
            projectFileOps.copyFileWithFeaturesRemoved(projectFileRemovedLane, projectFileRemovedFeatures, featuresToRemove)
         
            featureId = str(count).zfill(3) 
            
            # Run command            
            command = runCommand +\
            ' --headless' +\
            ' --tree-count='+str(TREE_NUM) +\
            ' --retrain' +\
            ' --label-proportion='+str(parsedArgs.label_proportion) +\
            ' --variable-importance-path='+path +\
            ' --export_source=\"Simple Segmentation\"' +\
            ' --output_filename_format='+outFeaturesFile+featureId+'_features_segmentation.h5' +\
            ' --project='+projectFileRemovedFeatures +\
            ' '+dataFile +\
            ' 2>&1 | tee -a '+logFeaturesFile 
            
            print command
        
            # Open OS process and wait
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            retval = process.wait() 
 
    # Tests with increasing trees
    if parsedArgs.trees_test :        
        for tri in TREE_RANGE:        
            treeId =  str(tri).zfill(3)    
            
            # Run command 
            command = runCommand +\
            ' --headless' +\
            ' --tree-count='+str(tri) +\
            ' --retrain' +\
            ' --label-proportion='+str(parsedArgs.label_proportion) +\
            ' --export_source=\"Simple Segmentation\"' +\
            ' --output_filename_format='+outTreesFile+treeId+'_trees_segmentation.h5' +\
            ' --project='+projectFileRemovedLane +\
            ' '+dataFile +\
            ' 2>&1 | tee -a '+logTreesFile 
            
            print command
            
            # Open OS process and wait
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)      
            retval = process.wait() 


    # Generate report
    featuresReport = Report(logFeaturesFile)
    treesReport = Report(logTreesFile)

if __name__ == "__main__":
    # Uncomment for debugging
    #sys.argv.append('--run-command=/opt/local/miniconda/envs/ilastik-devel/run_ilastik.sh')
    #sys.argv.append('--project-file=/groups/branson/home/cervantesj/profiling/test/larvaeRemovedVideo.ilp')
    
    parser = argparse.ArgumentParser( description="Export video to HDF5 format." )
    
    parser.add_argument('--run-command', help='Ilastik run command (default: ./run_ilastik.sh).', default='./run_ilastik.sh')
    parser.add_argument('--project-file', help='Name of project file.', required=True)
    parser.add_argument('--label-proportion', help='Proportion of feature-pixels used to train the classifier.', default=1.0, type=float)
    parser.add_argument('--trees-test', help='Enable increasing-trees test.', action='store_true', default=True)
    parser.add_argument('--features-test', help='Enable feature-removal test.', action='store_true', default=True)
    
    parsedArgs, workflowCmdlineArgs = parser.parse_known_args()
    
    main(parsedArgs)

