import os
import numpy as np
import cv2
import natsort
import matplotlib.pyplot as plt
import datetime
import sys

from TransmissionMap import TransmissionComposition
from getAtomsphericLight import getAtomsphericLight
from getColorContrastEnhancement import ColorContrastEnhancement
from getRGBDarkChannel import getDarkChannel
from getSceneRadiance import SceneRadiance


######################## Based on the DCP and the 0.1% brightest point is incorrect ########################
######################## Based on the DCP and the 0.1% brightest point is incorrect ########################
######################## Based on the DCP and the 0.1% brightest point is incorrect  and further cause the distortion of the restored images ########################
from getTransmissionEstimation import getTransmissionMap

def main(firstCall=1 , tag=1):
   
    folder=os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
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
            

            blockSize = 9
    
            imgGray = getDarkChannel(img, blockSize)
            AtomsphericLight = getAtomsphericLight(imgGray, img, meanMode=True, percent=0.001)
            # print('AtomsphericLight',AtomsphericLight)
            transmission = getTransmissionMap(img, AtomsphericLight, blockSize)
            sceneRadiance = SceneRadiance(img, AtomsphericLight, transmission)
            sceneRadiance = ColorContrastEnhancement(sceneRadiance)
            
            if(int(tag)):
                h,w,c = sceneRadiance.shape 
             
                if (int(firstCall)):
                    cv2.putText(sceneRadiance, '_LowComplexityDCP', (0,h-10) ,cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 2 )
                else:
                    cv2.putText(sceneRadiance, '_LowComplexityDCP', (0,h-30) ,cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 2 )
            
            #cv2.imwrite(os.path.join(folder,'OutputImages',(prefix + '_LowComplexityDCPMap.jpg')), np.uint8(transmission * 255))
            cv2.imwrite(os.path.join(folder,'OutputImages',(prefix + '_LowComplexityDCP.jpg')), sceneRadiance)
    
      
    
np.seterr(over='ignore')
if __name__ == '__main__':
    starttime = datetime.datetime.now()
    if len(sys.argv) > 1:
        main(sys.argv[1], sys.argv[2])
    else:
        main(0,1)
    Endtime = datetime.datetime.now()
    Time = Endtime - starttime
    print('Time', Time)
