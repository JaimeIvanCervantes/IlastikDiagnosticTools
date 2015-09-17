import h5py
import numpy as np
import re


class ProjectFileOps():
    
    # Copy project file with selected features deactivated.
    def copyFileWithFeaturesRemoved(self, fileNameIn, fileNameOut, features):
        fileIn = h5py.File(fileNameIn,'r')
        fileOut = h5py.File(fileNameOut,'w')
        
        fileIn.copy('Batch Inputs', fileOut) 
        fileIn.copy('Batch Prediction Output Locations', fileOut) 
        fileIn.copy('Input Data', fileOut) 
        fileIn.copy('PixelClassification', fileOut)
        fileIn.copy('Prediction Export', fileOut) 
        fileIn.copy('ProjectMetadata', fileOut) 
        fileIn.copy('currentApplet', fileOut) 
        fileIn.copy('ilastikVersion', fileOut) 
        fileIn.copy('time', fileOut) 
        fileIn.copy('workflowName', fileOut) 
        
        groupPath = fileIn['FeatureSelections/FeatureIds'].parent.name 
        groupId = fileOut.require_group(groupPath)
        fileIn.copy('FeatureSelections/FeatureIds', groupId, name="FeatureIds")
        
        groupPath = fileIn['FeatureSelections/Scales'].parent.name 
        groupId = fileOut.require_group(groupPath)
        fileIn.copy('FeatureSelections/Scales', groupId, name="Scales")
        
        groupPath = fileIn['FeatureSelections/StorageVersion'].parent.name 
        groupId = fileOut.require_group(groupPath)
        fileIn.copy('FeatureSelections/StorageVersion', groupId, name="StorageVersion")
        
        featureMatrix = fileIn['FeatureSelections/SelectionMatrix']
        
        featureMatrixData = np.array(featureMatrix)

        for feature in features :
            featureMatrixData[feature[0]][ feature[1]]  = False 
            
        print featureMatrixData
        
        fileOut.create_dataset('FeatureSelections/SelectionMatrix', shape = featureMatrix.shape, dtype=featureMatrix.dtype, data=featureMatrixData)
        fileOut.close()
        fileIn.close()
        
 
    # Remove the last lane (video) from the project file in order to conduct cross-validation
    def removeLastLane(self, fileNameIn, fileNameOut):
        fileNameToDelete = None
        
        fileIn = h5py.File(fileNameIn,'r')
        fileOut = h5py.File(fileNameOut,'w')
        
        fileIn.copy('Batch Inputs', fileOut) 
        fileIn.copy('Batch Prediction Output Locations', fileOut) 
        fileIn.copy('FeatureSelections', fileOut) 
        #fileIn.copy('Input Data', fileOut) 
        #fileIn.copy('PixelClassification', fileOut)
        fileIn.copy('Prediction Export', fileOut) 
        fileIn.copy('ProjectMetadata', fileOut) 
        fileIn.copy('currentApplet', fileOut) 
        fileIn.copy('ilastikVersion', fileOut) 
        fileIn.copy('time', fileOut) 
        fileIn.copy('workflowName', fileOut) 
        
        groupPath = fileIn['Input Data/Role Names'].parent.name 
        groupId = fileOut.require_group(groupPath)
        fileIn.copy('Input Data/Role Names', groupId, name="Role Names")    
 
        groupPath = fileIn['Input Data/StorageVersion'].parent.name 
        groupId = fileOut.require_group(groupPath)
        fileIn.copy('Input Data/StorageVersion', groupId, name="StorageVersion")  

        groupPath = fileIn['Input Data/local_data'].parent.name 
        groupId = fileOut.require_group(groupPath)
        fileIn.copy('Input Data/local_data', groupId, name="local_data") 
 
        # Copy the labels for all the videos except for the last one (used for cross-validation).
        length = len(fileIn['Input Data/infos'])
         
        for i, groupName in enumerate(fileIn['Input Data/infos'].keys()):
            if i < length-1:
                groupPath = fileIn['Input Data/infos/' + groupName].parent.name 
                groupId = fileOut.require_group(groupPath)             
                fileIn.copy('Input Data/infos/' + groupName, groupId, name=groupName) 
            else:
                fileNameToDelete = fileIn['Input Data/infos/' + groupName + '/Raw Data/filePath'][...]
 
        groupPath = fileIn['PixelClassification/ClassifierFactory'].parent.name 
        groupId = fileOut.require_group(groupPath)
        fileIn.copy('PixelClassification/ClassifierFactory', groupId, name="ClassifierFactory")
        
        groupPath = fileIn['PixelClassification/LabelColors'].parent.name 
        groupId = fileOut.require_group(groupPath)
        fileIn.copy('PixelClassification/LabelColors', groupId, name="LabelColors")
        
        groupPath = fileIn['PixelClassification/LabelNames'].parent.name 
        groupId = fileOut.require_group(groupPath)
        fileIn.copy('PixelClassification/LabelNames', groupId, name="LabelNames")
        
        groupPath = fileIn['PixelClassification/PmapColors'].parent.name 
        groupId = fileOut.require_group(groupPath)
        fileIn.copy('PixelClassification/PmapColors', groupId, name="PmapColors")
        
        groupPath = fileIn['PixelClassification/StorageVersion'].parent.name 
        groupId = fileOut.require_group(groupPath)
        fileIn.copy('PixelClassification/StorageVersion', groupId, name="StorageVersion")

        # Copy the labels for all the videos except for the last one (used for cross-validation).
        length = len(fileIn['PixelClassification/LabelSets'])
 
        for i, groupName in enumerate(fileIn['PixelClassification/LabelSets'].keys()): 
            if i < length-1:   
                groupPath = fileIn['PixelClassification/LabelSets/' + groupName].parent.name 
                groupId = fileOut.require_group(groupPath)             
                fileIn.copy('PixelClassification/LabelSets/' + groupName, groupId, name=groupName)
        
        fileIn.close()
        fileOut.close()
        
        return fileNameToDelete
    
    # Removed labels in certain frame ranges     
    def removeRangeLabels(self, fileNameIn, fileNameOut, ranges):
        fileIn = h5py.File(fileNameIn,'r')
        fileOut = h5py.File(fileNameOut,'w')
        
        fileIn.copy('Batch Inputs', fileOut) 
        fileIn.copy('Batch Prediction Output Locations', fileOut) 
        fileIn.copy('FeatureSelections', fileOut) 
        fileIn.copy('Input Data', fileOut) 
        fileIn.copy('Prediction Export', fileOut) 
        fileIn.copy('ProjectMetadata', fileOut) 
        fileIn.copy('currentApplet', fileOut) 
        fileIn.copy('ilastikVersion', fileOut) 
        fileIn.copy('time', fileOut) 
        fileIn.copy('workflowName', fileOut) 
        
        groupPath = fileIn['PixelClassification/ClassifierFactory'].parent.name 
        groupId = fileOut.require_group(groupPath)
        fileIn.copy('PixelClassification/ClassifierFactory', groupId, name="ClassifierFactory")
        
        groupPath = fileIn['PixelClassification/LabelColors'].parent.name 
        groupId = fileOut.require_group(groupPath)
        fileIn.copy('PixelClassification/LabelColors', groupId, name="LabelColors")
        
        groupPath = fileIn['PixelClassification/LabelNames'].parent.name 
        groupId = fileOut.require_group(groupPath)
        fileIn.copy('PixelClassification/LabelNames', groupId, name="LabelNames")
        
        groupPath = fileIn['PixelClassification/PmapColors'].parent.name 
        groupId = fileOut.require_group(groupPath)
        fileIn.copy('PixelClassification/PmapColors', groupId, name="PmapColors")
        
        groupPath = fileIn['PixelClassification/StorageVersion'].parent.name 
        groupId = fileOut.require_group(groupPath)
        fileIn.copy('PixelClassification/StorageVersion', groupId, name="StorageVersion")
        
        for groupName in fileIn['PixelClassification/LabelSets'].keys():  
            for dsetName, dset in fileIn['PixelClassification/LabelSets/'+groupName].items() :
                shapeString = dset.attrs['blockSlice']
            
                res = re.split('[,:\[\]]',shapeString)
                
                if int(res[1]) not in ranges :
                    groupPath = fileIn['PixelClassification/LabelSets/' + groupName + '/' + dsetName].parent.name 
                    groupId = fileOut.require_group(groupPath)             
                    fileIn.copy('PixelClassification/LabelSets/' + groupName + '/' + dsetName, groupId, name=dsetName)
        
        fileIn.close()
        fileOut.close()