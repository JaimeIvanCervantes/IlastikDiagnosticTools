# -*- coding: utf-8 -*-

import numpy as np
import csv
import StringIO
import operator

FEATURES_ABBR = {'Gaussian Smoothing' : 'GS', \
            'Laplacian of Gaussian' : 'LG', \
            'Gaussian Gradient Magnitude' : 'GGM', \
            'Difference of Gaussians' : 'DG', \
            'Structure Tensor Eigenvalues' : 'STE', \
            'Hessian of Gaussian Eigenvalues' : 'HGE'}

FEATURES_TIMES_TABLE = '''
STE(10.0), 0.0899804176082
HGE(10.0), 0.0759122723939
STE(5.0), 0.0585870499102
STE(3.5), 0.0502897465603
HGE(5.0), 0.048321234926
HGE(3.5), 0.0459901556657
GGM(10.0), 0.0405358385673
STE(1.6), 0.0389894226391
LG(10.0), 0.0388900119505
DG(10.0), 0.0384490596577
STE(1.0), 0.037961476452
HGE(1.6), 0.0353871715588
STE(0.7), 0.0352923477951
HGE(1.0), 0.0333979064015
HGE(0.7), 0.0318309108386
GGM(5.0), 0.0247910113118
GS(10.0), 0.0236307434648
GGM(3.5), 0.0233999997232
LG(5.0), 0.0232858693749
DG(5.0), 0.0207768114265
LG(3.5), 0.019847674264
DG(3.5), 0.01678671005
GS(5.0), 0.0133909389256
GGM(1.6), 0.0124198591635
LG(1.6), 0.0115737119261
DG(1.6), 0.0112218511991
GGM(1.0), 0.0111430601451
GS(3.5), 0.0110322203384
GGM(0.7), 0.0101948369526
LG(1.0), 0.00983127405315
DG(1.0), 0.0096541934168
GS(0.3), 0.00905669762266
LG(0.7), 0.00897762018094
DG(0.7), 0.00853874649048
GS(1.6), 0.0077524726097
GS(1.0), 0.00666786277455
GS(0.7), 0.00621081166133
'''

FEATURES_COORDINATES = { "GS(0.3)" : (0,0), \
                  "GS(0.7)" : (0,1), \
                  "GS(1.0)" : (0,2), \
                  "GS(1.6)" : (0,3), \
                  "GS(3.5)" : (0,4), \
                  "GS(5.0)" : (0,5), \
                  "GS(10.0)" : (0,6), \
                  "LG(0.7)" : (1,1), \
                  "LG(1.0)" : (1,2), \
                  "LG(1.6)" : (1,3), \
                  "LG(3.5)" : (1,4), \
                  "LG(5.0)" : (1,5), \
                  "LG(10.0)" : (1,6), \
                  "GGM(0.7)" : (2,1), \
                  "GGM(1.0)": (2,2), \
                  "GGM(1.6)" : (2,3), \
                  "GGM(3.5)" : (2,4), \
                  "GGM(5.0)" : (2,5), \
                  "GGM(10.0)" : (2,6), \
                  "DG(0.7)" : (3,1), \
                  "DG(1.0)": (3,2), \
                  "DG(1.6)" : (3,3), \
                  "DG(3.5)" : (3,4), \
                  "DG(5.0)" : (3,5), \
                  "DG(10.0)" : (3,6), \
                  "STE(0.7)" : (4,1), \
                  "STE(1.0)" : (4,2), \
                  "STE(1.6)" : (4,3), \
                  "STE(3.5)" : (4,4), \
                  "STE(5.0)" : (4,5), \
                  "STE(10.0)" : (4,6), \
                  "HGE(0.7)" : (5,1), \
                  "HGE(1.0)" : (5,2), \
                  "HGE(1.6)" : (5,3), \
                  "HGE(3.5)" : (5,4), \
                  "HGE(5.0)" : (5,5), \
                  "HGE(10.0)" : (5,6) } 

class FeatureParser() :
    def _strip_non_ascii(self, string):
        ''' Returns the string without non ASCII characters'''
        stripped = (c for c in string if 0 < ord(c) < 127)
        return ''.join(stripped)
    
    
    def getFeatures(self, file_name = None, features_importance_table = None ):
        
        if file_name != None :
            with open(file_name,'r') as file :
                features_importance_table = file.readlines()
                features_importance_table = "".join(features_importance_table)
        
        features_importance_table = features_importance_table.splitlines()
        features_importance_table = "\n".join(features_importance_table[1:])       
        features_importance_table = self._strip_non_ascii(features_importance_table)
        
        print features_importance_table
        
        f = StringIO.StringIO(features_importance_table)
        reader = csv.reader(f, delimiter=',')
        
        features_importances = {}
        
        importances_total = 0.0;
        
        for row in reader:  
            if len(row) < 4 :
                continue
        
            tokens = row[0].split('(=')
        
            feature = tokens[0].strip()
            feature = FEATURES_ABBR[feature]
                      
            sigma = (tokens[1].split(')'))[0]
            sigma.strip()
                      
            feature = feature + '(' + sigma + ')'    
            
            if feature in features_importances :
                features_importances[feature] += float(row[3])
            else :
                features_importances[feature] = float(row[3])
        
        importances_total = sum([tuple[1] for tuple in features_importances.items()])
        
        for feature, importance in features_importances.items():
            features_importances[feature] = importance/importances_total
        
        # Get feature times dictionary
        f = StringIO.StringIO(FEATURES_TIMES_TABLE)
        reader = csv.reader(f, delimiter=',')
        
        features_times = {}
        
        for row in reader:  
            if len(row) < 2 :
                continue
            
            features_times[row[0].strip()] = float(row[1].strip())
        
        # Get feature scores
        features_scores = {} 
        
        for feature in features_importances.keys() :
        #for feature in features_times.keys() :
            features_scores[feature] = 1.5 + ( 1.0*features_times[feature] - 1.5*features_importances[feature] ) 
            
        # Return features to remove
        #features_sorted_by_score = sorted(features_scores.items(), key=operator.itemgetter(1) , reverse=True)
        features_sorted_by_importance = sorted(features_importances.items(), key=operator.itemgetter(1) , reverse=False)
           
        
        #[tuple[1] for tuple in features_importances.items()]
        
        features_coordinates = []
        
        for tuple in features_sorted_by_importance :
            features_coordinates.append( (tuple[0], FEATURES_COORDINATES[tuple[0]]) )    
        
        #for tuple in features_sorted_by_score :
        #    features_coordinates.append( (tuple[0], FEATURES_COORDINATES[tuple[0]]) )
            
        return features_coordinates


     

