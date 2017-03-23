# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 19:46:04 2017

@author: Niranjan
"""

import nltk 
import numpy as np
import pandas as pd
from nltk.corpus import wordnet
import csv
from sklearn.ensemble import RandomForestClassifier
from Levenshtein import *
from difflib import SequenceMatcher

quora_data = pd.read_csv("F:\\Study\\OneDrive - The University of Texas at Dallas\\02 Study\\06 Quora\\train.csv")
quora_data["levenshtein_dist"] = 0
quora_data['question1']



def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()



quora_data_train = []
fname = "C:\\Users\\Niranjan\\Desktop\\train.csv"
with open(fname, encoding="utf8",newline='') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        leven_distance = distance(row[3],row[4])
        similarity_dist = round(similar(row[3],row[4]),6)
        list_data = [ row[3],row[4],leven_distance,similarity_dist,row[5]]
        quora_data_train.append(list_data)
        
      
quora_data_train = pd.DataFrame(quora_data_train)
quora_data_train.columns = quora_data_train.iloc[0]
quora_data_train = quora_data_train.drop(quora_data_train.index[0])
quora_data_train = quora_data_train.rename(columns = {1 : "Similarity", 0.888889  : "Similar_distance"})
print(quora_data_train[:10])

quora_data_train.columns

quora_data_test = []
fname = "C:\\Users\\Niranjan\\Desktop\\test.csv"
with open(fname, encoding="utf8",newline='') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        leven_distance = distance(row[1],row[2])
        similarity_dist = round(similar(row[1],row[2]),6)
        list_data = [ row[1],row[2],leven_distance,similarity_dist]
        quora_data_test.append(list_data)
        
   
quora_data_test = pd.DataFrame(quora_data_test)
quora_data_test.columns = quora_data_test.iloc[0]
quora_data_test = quora_data_test.drop(quora_data_test.index[0])
quora_data_test = quora_data_test.rename(columns = {1 : "Similarity", 0.888889  : "Similar_distance"})
print(quora_data_test[:2])

quora_data_train.to_csv("F:\\Study\\OneDrive - The University of Texas at Dallas\\02 Study\\06 Quora\\train_modified.csv")
quora_data_test.to_csv("F:\\Study\\OneDrive - The University of Texas at Dallas\\02 Study\\06 Quora\\test_modified.csv")

cols = ['Similarity','Similar_distance']
res_col = ['is_duplicate']

trainarr = quora_data_train.as_matrix(cols)
trainres = quora_data_train.as_matrix(res_col)

rf = RandomForestClassifier(n_estimators=100)
rf.fit(trainarr,trainres)

testarr = quora_data_test.as_matrix(cols)
results = rf.predict(testarr)

print(results[:5])
quora_data_test['is_duplicate'] = results
quora_data_test = quora_data_test.assign(test_id=[0 + i for i in range(len(quora_data_test))])

print(quora_data_test[:3])

quora_data_final = quora_data_test[['test_id','is_duplicate']]
print(quora_data_final[:3])
quora_data_final.shape
    

quora_data_final.to_csv("F:\\Study\\OneDrive - The University of Texas at Dallas\\02 Study\\06 Quora\\final_result.csv",index=False)

