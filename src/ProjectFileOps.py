import h5py
import numpy as np

class ProjectFileOps():
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
                
        for fti in range(len(features)) :
            featureMatrixData[ features[fti][1] ] = False
            
        print featureMatrixData
        
        fileOut.create_dataset('FeatureSelections/SelectionMatrix', shape = featureMatrix.shape, dtype=featureMatrix.dtype, data=featureMatrixData)
        fileOut.close()
        fileIn.close()
        
         
    def modifyLabels(self, fileNameIn, fileNameOut, ranges):
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
                
                if int(res[1]) == 0 or int(res[1]) == 48 :
                    groupPath = fileIn['PixelClassification/LabelSets/' + groupName + '/' + dsetName].parent.name 
                    groupId = fileOut.require_group(groupPath)             
                    fileIn.copy('PixelClassification/LabelSets/' + groupName + '/' + dsetName, groupId, name=dsetName)
        
        fileIn.close()
        fileOut.close()