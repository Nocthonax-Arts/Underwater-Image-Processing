import os
import numpy as np
import cv2
import natsort
import xlwt
import glob
import datetime
from subprocess import call


class CallPy(object):
    def __init__(self, path):
        self.path = path
    
    def callAlg(self, firstCall=1, tag=1):
        call(["Python", "{}".format(self.path), str(firstCall) , str(tag)]) 


#run all enhancement and color restoration algorithm on the input images
def doAlgs():
    
    #path to enhancement algorithm scripts, if u don't use the default recommended file structure, edit accordingly
    #recommended use of os.path. functions for cross-platform use 
    enh_path= os.path.join(os.path.dirname(__file__), 'Underwater_Image_Enhancement')
    
    #path to color restoration algorithm scripts, if u don't use the default recommended file structure, edit accordingly
    clr_path= os.path.join(os.path.dirname(__file__), 'Underwater_Image_Color_Restoration')
    
    
    #find all algorithm scripts in the Image Enhancement folder, store names of folders
    enhancer_names = []
    
    for entry_name in os.listdir(enh_path):
       entry_path = os.path.join(enh_path, entry_name)
       if os.path.isdir(entry_path):    
           if(entry_name !='Fusion-Matlab'):
               enhancer_names.append(entry_name)
    
    
    #run input images through all Enhancers
    enhancers= []
    
    for i in range(len(enhancer_names)):
        enhancers.append( CallPy(os.path.realpath(os.path.join(enh_path, enhancer_names[i], 'main.py'))))
        print('\nStarting Enhancement method: ', enhancer_names[i])
        enhancers[i].callAlg(1, 1)
    
    
    #find all algorithm scripts in the Image Enhancement, store names of folders
    clr_names = []
    
    for entry_name in os.listdir(clr_path):
        entry_path = os.path.join(clr_path, entry_name)
        if os.path.isdir(entry_path):    
                clr_names.append(entry_name)
        
    #run input images through all Color restoration algorithms    
    clrs= []    
    for i in range(len(clr_names)):
        clrs.append( CallPy(os.path.realpath(os.path.join(clr_path, clr_names[i], 'main.py'))))
        print('\nStarting Color restoration method: ', clr_names[i])
        clrs[i].callAlg(1,1)

#make compare maps, helper feature
def doMaps():
    
    map_path= os.path.join(os.path.dirname(__file__), '..' , 'OutputImages')
    map_names = []
    
    #find all file names in default output folder
    for file_name in os.listdir(map_path):
        file_path = os.path.join(map_path, file_name)
        if os.path.isfile(file_path):
            map_names.append(file_name)
                         
    in_path= os.path.join(os.path.dirname(__file__),'..' , 'InputImages')
    in_names = []
    
    #find all file names in default input folder
    for file_name in os.listdir(in_path):
        file_path = os.path.join(in_path, file_name)
        if os.path.isfile(file_path):
            in_names.append(file_name.split('.')[0])
                               
    #if files in output have same first word, connect them together
    #intended naming convention is using numbers for input images
    #input eg. 0001.png 0002.png ... 0324.png ... 1443.png
    #output images will add _Algorythm name to the end
    #output eg. 0001_clahe.png 0002_clahe.png ... 0324_clahe.png ... 1443_clahe.png
    
    for name in in_names:
        helper = [] 
        for i in range(len(map_names)):
            if name in map_names[i]:
                helper.append(cv2.imread(os.path.join(map_path,map_names[i])))
                
        print(len(helper))
        helper2 = []
        
    #connect images into one, for easier comparison
    #works only for multiples of 3 and 4 
    #for more flexible solution would be adding empty images to fill out the 
    #desired grid, but this is only a helper feature
        if(len(helper)%4 == 0):
    
            for g in range(3, len(helper), 4):
                helper2.append(cv2.hconcat([helper[g-3],helper[g-2],helper[g-1],helper[g]]))
            
        elif(len(helper)%3 == 0):
            
            for g in range(2, len(helper), 3):
                helper2.append(cv2.hconcat([helper[g-2],helper[g-1],helper[g]]))
            
            
    #print connected image
        imgt= cv2.vconcat(helper2)
        cv2.imwrite(os.path.join(map_path, (name + '_MIXMAP.jpg')),imgt) 

if __name__ == "__main__":
    doAlgs()
    doMaps()
        
