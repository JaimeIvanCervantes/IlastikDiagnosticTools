import h5py
import numpy as np
import matplotlib.pylab as plt
import os
import re
import string
from scipy.stats import norm
from scipy.stats import mode
import matplotlib.mlab as mlab


all_features = [ "GS(0.3)", "GS(0.7)", "GS(1.0)", "GS(1.6)", "GS(3.5)", "GS(5.0)", "GS(10.0)", "LG(0.7)", "LG(1.0)", "LG(1.6)", "LG(3.5)", "LG(5.0)", "LG(10.0)", "GGM(0.7)", "GGM(1.0)", "GGM(1.6)", "GGM(3.5)", "GGM(5.0)", "GGM(10.0)", "DG(0.7)", "DG(1.0)", "DG(1.6)", "DG(3.5)", "DG(5.0)", "DG(10.0)", "STE(0.7)", "STE(1.0)", "STE(1.6)", "STE(3.5)", "STE(5.0)", "STE(10.0)", "HGE(0.7)", "HGE(1.0)", "HGE(1.6)", "HGE(3.5)", "HGE(5.0)", "HGE(10.0)" ]

feature_mode = True


STOPPING_POINT = 0
LABELS_FILE = '/groups/branson/home/cervantesj/profiling/Alice/Courtship_Bowls/lab/gmr.h5'
#LABELS_FILE = '/misc/public/JaimeProfiling/Alice/Courtship_Bowls/lab/gmr.h5'
FEATURES_FILE = '/groups/branson/home/cervantesj/profiling/Alice/Courtship_Bowls/pred/5511280815.txt'
FEATURES_PRED_DIR = '/groups/branson/home/cervantesj/profiling/Alice/Courtship_Bowls/pred/5511280815_features/'
TREES_PRED_DIR = '/groups/branson/home/cervantesj/profiling/Alice/Courtship_Bowls/pred/3021230815_trees/'

# Open labels file
with h5py.File(LABELS_FILE,'r') as labelsFile:
    labels = labelsFile['exported_data']
    labels = np.array(labels)

if feature_mode :
    pred_dir = FEATURES_PRED_DIR
else :
    pred_dir = TREES_PRED_DIR
    
fileNames = os.listdir(pred_dir)#[f for f in os.listdir(pred_dir) if re.match(r'[0-9]+.*\.h5', f)]
#fileNames = os.listdir(predDir)

errors = []

# Get cross-validation error for each prediction file
count = 0
error_sel = 0

for fileName in sorted(fileNames):
    count += 1
    
    fullFileName =  pred_dir + fileName
    
    with h5py.File(fullFileName,'r') as imagesFile:
        images = imagesFile['exported_data']
        images = np.array(images)
    
    #plt.imshow(labels[49,:,:,0]+images[49,:,:,0])
    #plt.show()
             
    #match = labels[labels==2] == images[labels==2]          
    match = labels[labels!=0] == images[labels!=0]  
    error = 100.0*(float(len(match[match==False]))/float(len(match)))     
    errors.append(error)  
    
    print "File", fileName, " Error: ", error
    
    if STOPPING_POINT != 0 and count == STOPPING_POINT :
        error_sel = error
        plt.imshow(labels[49,:,:,0]+images[49,:,:,0])
        print "Error at Point Selected: ", error_sel
        plt.show()
        

# Get stats
modes, bins = mode(errors)
mode = modes[0]
(mu, sigma) = norm.fit(errors)
print "mu: ", mu
print "mode: ", mode
print "sigma: ", sigma
print "max: ", max(errors)
print "min: ", min(errors)

mu_array = np.full(len(errors), mu)
mod_array = np.full(len(errors), mode)
sigma_array = np.full(len(errors), sigma + mode)

hist, bin_edges = np.histogram(errors, bins = np.arange(min(errors),max(errors), 0.01))
norm = mlab.normpdf( bin_edges, mu, sigma)

# Plot results
#plt.figure(figsize=(13.841, 7.195), dpi=100)

#plt.xlabel('Features Removed')
#plt.ylabel('Cross-validation Error (%)')
#plt.title('Feature Removal Test (Alice\'s Fly-Bubble)')

plt.xlabel('Number of Trees')
plt.ylabel('Cross-validation Error (%)')
plt.title('Error Tests')

x = range(len(errors))
x = x + np.full(len(errors),1)

#print len(bin_edges[0:-1])
#print len(hist[0:-2])
#plt.hist(errors, bins=25, normed=True, alpha=0.6, color='g')
#plt.plot(bin_edges, norm, 'r--')
#plt.plot(range(len(errors)), errors, 'b-', bin_edges[0:-1], [0:-1], 'r--')
#plt.plot(x, errors, 'bo-', x, mod_array, 'g--', x, sigma_array, 'r--', x, mu_array, 'k--' )
#plt.xlim(xmin=1, xmax=55)
plt.plot(x, errors, 'bo-')

if feature_mode :
    with open(FEATURES_FILE) as file:
        labels = file.readline()
    
    labels = labels.strip()
    print labels
    
    labels = string.split(labels,', ')
    
    missing_label = ''
    
    for feature in all_features :
        if feature not in labels:
            missing_label = feature
    
    print "Missing Label: ", missing_label
    
    labels.append(missing_label)
    
    labels_missing_str = ''
    labels_selected_str = ''
    
    count = 0
    for i in range(STOPPING_POINT) :
        if i == 0 :
            labels_missing_str = labels[i]
        elif count % 3 != 0 :
            labels_missing_str = labels_missing_str + ', ' + labels[i]
        elif count % 3 == 0 :
            labels_missing_str = labels_missing_str + '\n' + labels[i]
            
        count += 1
    
        
    print 'Labels Missing: \n', labels_missing_str   
    
    count = 0    
    for i in range(STOPPING_POINT, len(labels)) :
        if i == 0 :
            labels_selected_str = labels[i]
        elif count % 3 != 0 :
            labels_selected_str = labels_selected_str + ', ' + labels[i]
        elif count % 3 == 0 :
            labels_selected_str = labels_selected_str + '\n' + labels[i]
            
        count += 1
    
    print '\nLabels Selected:', labels_selected_str
    
    
    ticks = ['']
    
    count = 0
    
    for lab_i in range(len(labels)) :
        tick = ''
        for lab_j in range(lab_i) :
            if tick == '' :
                tick += labels[lab_j]
            elif lab_j % 2 == 0 :
                tick += ',' + labels[lab_j]
            elif lab_j % 2 == 1 :
                tick += '\n' + labels[lab_j]
                
        if lab_i == 1 or lab_i % 5 == 0 :
            ticks.append(tick)
        else :
            ticks.append(' ')
  
#plt.tick_params(axis='both', which='major', labelsize=8)
#plt.xticks(x, ticks, rotation='vertical')
plt.show()
        
'''
