import os
import numpy as np
import cv2
import natsort
import sys
import datetime

from LabStretching import LABStretching
from global_stretching_RGB import stretching

def RGHS(sceneRadiance):
    
    height = len(sceneRadiance)
    width = len(sceneRadiance[0])
 
    sceneRadiance = stretching(sceneRadiance)
    sceneRadiance = LABStretching(sceneRadiance)

    return sceneRadiance
    
def HE(sceneRadiance):
    
    for i in range(3):
        sceneRadiance[:, :, i] =  cv2.equalizeHist(sceneRadiance[:, :, i])
     
    return sceneRadiance
    
def CLAHE(sceneRadiance):
    
    clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(4, 4))
    for i in range(3):
        sceneRadiance[:, :, i] = clahe.apply((sceneRadiance[:, :, i]))

    return sceneRadiance
    
    
def main(tag=1):
    
    folder=os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..'))
    path = os.path.join(folder,"InputImages")
    files = os.listdir(path)
    files =  natsort.natsorted(files)
    
    for i in range(len(files)):
        file = files[i]
        filepath = os.path.join(path, file)
        prefix = file.split('.')[0]
        if os.path.isfile(filepath):
            print('********    file   ********',file)
            img = cv2.imread(os.path.join(folder,"InputImages", file))
            
            
            claheImg= CLAHE(img);
            print('******** CLAHE ********    file   ********',file, )
            
            rghsImg= RGHS(claheImg);
            print('******** RGHS ********    file   ********',file, )
            
            he_Img= HE(claheImg);
            print('******** HE ********    file   ********',file, )
            
            if(int(tag)):
                h,w,c = claheImg.shape 
                cv2.putText(rghsImg, '_CLAHE_RGHS', (0,h-10) ,cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 2 )
                cv2.putText(he_Img, '_CLAHE_HE', (0,h-10) ,cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 2 )
                
            cv2.imwrite(os.path.join(folder,'OutputImages',(prefix + '_CLAHE_RGHS.jpg')), rghsImg)
            cv2.imwrite(os.path.join(folder,'OutputImages',(prefix + '_CLAHE_HE.jpg')), he_Img)
            
np.seterr(over='ignore')
if __name__ == '__main__':
    starttime = datetime.datetime.now()
    
    main()
    
    Endtime = datetime.datetime.now()
    Time = Endtime - starttime
    print('Time', Time)
    