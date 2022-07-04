import math
import os
import natsort
import numpy as np
import datetime
import cv2
import sys
from skimage.color import rgb2hsv


from color_equalisation import RGB_equalisation
from global_stretching_RGB import stretching
from hsvStretching import HSVStretching

from histogramDistributionLower import histogramStretching_Lower
from histogramDistributionUpper import histogramStretching_Upper
from rayleighDistribution import rayleighStretching
from rayleighDistributionLower import rayleighStretching_Lower
from rayleighDistributionUpper import rayleighStretching_Upper
from sceneRadiance import sceneRadianceRGB

e = np.e
esp = 2.2204e-16


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
            
            height = len(img)
            width = len(img[0])
    
            sceneRadiance = RGB_equalisation(img, height, width)
            # sceneRadiance = stretching(img)
            sceneRadiance = stretching(sceneRadiance)
            sceneRadiance_Lower, sceneRadiance_Upper = rayleighStretching(sceneRadiance, height, width)
    
            sceneRadiance = (np.float64(sceneRadiance_Lower) + np.float64(sceneRadiance_Upper)) / 2
    
    
            sceneRadiance = HSVStretching(sceneRadiance)
            sceneRadiance = sceneRadianceRGB(sceneRadiance)
            
            if(int(tag)):
                h,w,c = sceneRadiance.shape 
                 
                if (int(firstCall)):
                    cv2.putText(sceneRadiance, '_RayleighDistribution', (0,h-10) ,cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 2 )
                else:
                    cv2.putText(sceneRadiance, '_RayleighDistribution', (0,h-30) ,cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 2 )
    
            
            cv2.imwrite(os.path.join(folder,'OutputImages',(prefix + '_RayleighDistribution.jpg')), sceneRadiance)
         

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
