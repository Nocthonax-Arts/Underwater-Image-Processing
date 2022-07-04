import os
import numpy as np
import cv2
import natsort
import xlwt
import sys
import datetime
from global_histogram_stretching import stretching
from hsvStretching import HSVStretching
from sceneRadiance import sceneRadianceRGB


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
        
            img = stretching(img)
            sceneRadiance = sceneRadianceRGB(img)
            sceneRadiance = HSVStretching(sceneRadiance)
            sceneRadiance = sceneRadianceRGB(sceneRadiance)
        
        
            if(int(tag)):
                    h,w,c = sceneRadiance.shape 
                 
                    if (int(firstCall)):
                        cv2.putText(sceneRadiance, '_ICM', (0,h-10) ,cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 2 )
                    else:
                        cv2.putText(sceneRadiance, '_ICM', (0,h-30) ,cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 2 )
    
            
            cv2.imwrite(os.path.join(folder,'OutputImages',(prefix + '_ICM.jpg')), sceneRadiance)
     
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