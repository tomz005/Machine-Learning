# -*- coding: utf-8 -*-
"""q2_code.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KIVfxSTZze0ZcVTkPN6ROFSiONG8rhwI
"""

# from google.colab import drive
# drive.mount('/content/drive')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import operator
import collections
from sklearn.metrics import accuracy_score,confusion_matrix
from sklearn.metrics import recall_score,precision_score,f1_score
from scipy import stats
from sklearn.neighbors import KNeighborsClassifier

class KNNClassifier:

  def __init__(self):
    self.attributes=[['b','c','x','f','k','s'],
                     ['f','g','y','s'],
                     ['n','b','c','g','r','p','u','e','w','y'],
                     ['t','f'],
                     ['a','l','c','y','f','m','n','p','s'],
                     ['a','d','f','n'],
                     ['c','w','d'],
                     ['b','n'],
                     ['k','n','b','h','g','r','o','p','u','e','w','y'],
                     ['e','t'],
                     ['b','c','u','e','z','r'],
                     ['f','y','k','s'],
                     ['f','y','k','s'],
                     ['n','b','c','g','o','p','e','w','y'],
                     ['n','b','c','g','o','p','e','w','y'],
                     ['p','u'],
                     ['n','o','w','y'],
                     ['n','o','t'],
                     ['c','e','f','l','n','p','s','z'],
                     ['k','n','b','h','r','o','u','w','y'],
                     ['a','c','n','s','v','y'],
                     ['g','l','m','p','u','w','d']]
    self.distances=[]
    self.k=5
    # self.train_attributes
    # # sum=0
    # for i in range(0,22):
    #   print(len(self.attributes[i]))
    # # print(sum)

  def calculate_distance(self,param):
    if(param==1):
        #Euclidean Distance
        for i in self.test_attributes:
            for j in self.train_attributes:
                euclid_distance=np.sum((i-j)**2)
                self.distances.append(euclid_distance)

    else:
        #Manhattan Distance
        for i in self.test_attributes:
          for j in self.train_attributes:
            manhatten_distance=np.sum(abs(i-j))
            self.distances.append(manhatten_distance)

  def predict_label(self,list_k):
    votes={}
    for i in range(len(list_k)):
        response=list_k[i][1];
        if(response in votes):
            votes[response]+=1
        else:
            votes[response]=1
    # print(votes)
    sorted_votes=sorted(votes.items(),key=lambda item: item[1])
    # print(sorted_votes)
    return sorted_votes[len(sorted_votes)-1][0]

  def train(self,trainfilepath):
    data=pd.read_csv(trainfilepath,header=None)
    data_array=data.to_numpy()
    # print(data_array)
    attributeinfo=np.delete(data_array,0,1)
    addrow=attributeinfo[0,:]
    # print(type(attributeinfo))
    label=data_array[:,0]
    #Finding count of ? values in column 11
    # print(collections.Counter(attributeinfo[:,10]))
    mode=stats.mode(attributeinfo[:,10])
    # print(mode[0][0])
    for i in range(len(attributeinfo)):
      if(attributeinfo[i,10]=='?'):
        attributeinfo[i,10]=mode[0][0]

    # print(attributeinfo)
    originallength=len(attributeinfo)
    for i in range(0,22):
      # print(i)
      # print(np.unique(attributeinfo[:,i]))
      # print(np.asarray(self.attributes[i]))
      difference=np.setdiff1d(np.asarray(self.attributes[i]),np.unique(attributeinfo[:,i]))
      # print(difference)
      if(len(difference)>0):
        for element in difference:
          addrow[i]=element
          attributeinfo=np.vstack([attributeinfo,addrow])

    attributeinfo_df=pd.DataFrame()

    # print(originallength)
    for i in range(0,22):
      attributeinfo_onehot=pd.get_dummies(attributeinfo[:,i])
      # print(attributeinfo_onehot)
      attributeinfo_df=pd.concat([attributeinfo_df,attributeinfo_onehot],axis=1)
    # print(len(attributeinfo_df))
    processed_df=attributeinfo_df.iloc[0:originallength,:]
    # print(processed_df)
    # processed_df['Label']=label
    processed_df.insert(0,'Label',label)
    # print(processed_df)
    # print(processed_df.iloc[1606,:])
    # attributeinfo_df.to_csv('q21hot.csv')
    # print(type(X))
    # print(Y)
    # Splitting data into train & validate
    # msk = np.random.rand(len(processed_df)) < 0.8
    self.train_df = processed_df
    # validation_df = processed_df[~msk]
    # print(len(processed_df))
    # print(len(self.train_df))
    # print(train_df)
    # print(len(validation_df))
    # print(validation_df)
    train_array=self.train_df.to_numpy()
    self.train_labels=train_array[:,0]
    self.train_attributes=train_array[:,1:]
    # validation_array=validation_df.to_numpy()
    # self.validation_labels=validation_array[:,0]
    # self.validation_attributes=validation_array[:,1:]
    # print("Distance calculation started")
    # self.calculate_distance(1)
    # print("Distance calculation complete")
    # print(len(self.distances))
    # print(self.train_labels)
    # print(self.train_attributes[0,:])
  def predict(self,testfilepath):
    predicted_list=[]
    list_k=[]
    accuracy=[]
    precision=[]
    recall=[]
    f1score=[]
    kvalue=[]
    testdata=pd.read_csv(testfilepath,header=None)
    testdata_array=testdata.to_numpy()
    addrow=testdata_array[0,:]
    mode=stats.mode(testdata_array[:,10])
    # print(mode[0][0])
    for i in range(len(testdata_array)):
      if(testdata_array[i,10]=='?'):
        testdata_array[i,10]=mode[0][0]
    originallength=len(testdata_array)
    for i in range(0,22):
      # print(i)
      # print(np.unique(attributeinfo[:,i]))
      # print(np.asarray(self.attributes[i]))
      difference=np.setdiff1d(np.asarray(self.attributes[i]),np.unique(testdata_array[:,i]))
      # print(difference)
      if(len(difference)>0):
        for element in difference:
          addrow[i]=element
          testdata_array=np.vstack([testdata_array,addrow])

    testdata_df=pd.DataFrame()

    for i in range(0,22):
      attributeinfo_onehot=pd.get_dummies(testdata_array[:,i])
      # print(attributeinfo_onehot)
      testdata_df=pd.concat([testdata_df,attributeinfo_onehot],axis=1)
    # print(len(attributeinfo_df))
    processedtest_df=testdata_df.iloc[0:originallength,:]

    self.test_attributes=processedtest_df.to_numpy()

    print("Distance calculation started")
    self.calculate_distance(1)
    print("Distance calculation complete")
    print(len(self.distances))


    for i in range(0,len(self.distances),len(self.train_attributes)):
      for j in range(i+0,i+len(self.train_attributes)):
          list_k.append((self.distances[j],self.train_labels[j%len(self.train_attributes)]))
          if(len(list_k)>self.k):
              list_k.sort()
              list_k=list_k[:self.k]
      predicted_list.append(self.predict_label(list_k))
      list_k.clear()
      # for i in range(len(predicted_list)):
        # print(self.validation_labels[i],predicted_list[i])
    # accuracy.append(accuracy_score(self.validation_labels,predicted_list))
    # precision.append(precision_score(self.validation_labels,predicted_list,average='macro'))
    # recall.append(recall_score(self.validation_labels,predicted_list,average='macro'))
    # f1score.append(f1_score(self.validation_labels,predicted_list,average='macro'))
    # kvalue.append(k)
    return predicted_list
    # predicted_list.clear()

    # print(kvalue)
    # print(accuracy)
    # # print(precision)
    # # print(recall)
    # # print(f1score)
    # plt.plot(kvalue,accuracy)
    # plt.xlabel('K value')
    # plt.ylabel('Accuracy')
    # plt.show()

  def sklearn_knn(self):
    score=[]
    kv=[]
    print("Scikit lean KNN Accuracy")
    for k in range(2,20,1):
      knn=KNeighborsClassifier(n_neighbors=k)
      knn.fit(self.train_attributes,self.train_labels)
      predicted_labels=knn.predict(self.validation_attributes)
      score.append(accuracy_score(self.validation_labels,predicted_labels))
      kv.append(k)
    plt.plot(kv,score)
    plt.xlabel('K value')
    plt.ylabel('Accuracy')
    plt.show()

# trainfilename='/content/drive/My Drive/Datasets/q2/train.csv'
# testfilename='/content/drive/My Drive/Datasets/q2/test.csv'
# testlabelpath='/content/drive/My Drive/Datasets/q2/test_labels.csv'
#   # data=pd.read_csv(filename)
# knc=KnnClassifier()
# knc.train(trainfilename)
# predictions=knc.predict(testfilename)
# # knc.sklearn_knn()
# # predictions = knn_classifier.predict('./Datasets/q1/test.csv')
# val=pd.read_csv(testlabelpath,header=None)
# vala=val.to_numpy()
# test_labels = vala[:,0]
# print (accuracy_score(test_labels, predictions))
