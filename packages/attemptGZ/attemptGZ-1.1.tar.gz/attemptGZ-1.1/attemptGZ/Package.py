import sys       
import cv2
import sys
import time
import datetime
import os
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib import image
from matplotlib.cbook import get_sample_data
from PIL import Image
import pandas as pd
from random import randint
from numpy import random

import shutil as shutil



class Images():
    def __init__(self,n):

    
        self.n = n
        self.crop = 84
        
        self.homeDir = sys.path[6] +'/attemptGZ'
        self.dataDir = self.homeDir + '/IMAGES'
        
    def getClasses(self):
       
        os.chdir(self.homeDir)
        labels = pd.read_csv( 'classification_labels_train.csv');
        
        cigar=  np.array(labels[labels['Class7.3']==1].GalaxyID)
        middle= np.array(labels[labels['Class7.2']==1].GalaxyID)
        roundd= np.array(labels[labels['Class7.1']==1].GalaxyID)
        
        return np.array([cigar, middle, roundd],dtype = 'object')
              
    
    def getData(self,galaxyClass,n,crop,directory):
        os.chdir(directory)
        files=[]
        filetype = os.listdir()[0][-4:]

        for i in range(len(galaxyClass)):
            if galaxyClass[i] != '.DS_Store':
                files.append(str(galaxyClass[i])+str(filetype))
        del i

        np.random.shuffle(files)
        sample= files[0:n]

        shape= np.array([n,424-crop*2,424-crop*2,3])
        mult= 1
        for i in range(len(shape)):
            mult*=shape[i]
        del i


        images = np.zeros(mult).reshape(shape) 

        for i in range(len(sample)):

            img=  image.imread(sample[i])
            img = img[crop : -1*crop , crop : -1*crop]
            img = cv2.normalize(img, None, 0, 1.0, cv2.NORM_MINMAX, dtype=cv2.CV_32F)
            img = np.expand_dims(img, axis=0)
            images[i] = img
        del i
        return images
        
    def getQuick(self):
        n=self.n
        crop= self.crop
        directory= self.dataDir
        np.random.seed(np.random.randint(0,100000))
        classes = self.getClasses()
    
        cigar   = self.getData(classes[0] ,n,crop, directory)
        middle = self.getData(classes[1],n,crop, directory)
        roundd   = self.getData(classes[2],n,crop, directory)

        train=np.concatenate((cigar,roundd,middle))
        np.random.shuffle(train)
        
        return train





