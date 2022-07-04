import os
import datetime
import numpy as np
import cv2
import natsort
import sys

from DetermineDepth import determineDepth
from TransmissionEstimation import getTransmission
from getAdaptiveExposureMap import AdaptiveExposureMap
from getAdaptiveSceneRadiance import AdaptiveSceneRadiance
from getAtomsphericLight import getAtomsphericLight
from refinedTransmission import refinedtransmission

from sceneRadianceGb import sceneRadianceGB
from sceneRadianceR import sceneradiance

# # # # # # # # # # # # # # # # # # # # # # Normalized implement is necessary part as the fore-processing   # # # # # # # # # # # # # # # #

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
            
            img = (img - img.min()) / (img.max() - img.min()) * 255
            blockSize = 9
            largestDiff = determineDepth(img, blockSize)
            AtomsphericLight, AtomsphericLightGB, AtomsphericLightRGB = getAtomsphericLight(largestDiff, img)
            print('AtomsphericLightRGB',AtomsphericLightRGB)
            
            # transmission = getTransmission(img, AtomsphericLightRGB, blockSize=blockSize)
            transmission = getTransmission(img, AtomsphericLightRGB, blockSize)
            # print('transmission.shape',transmission.shape)
            # TransmissionComposition(folder, transmission, number, param='coarse')
            transmission = refinedtransmission(transmission, img)
    
            #cv2.imwrite(os.path.join(folder,'OutputImages',(prefix + '_GBDehazedRcoorectionUDCP_TM.jpg')), np.uint8(transmission[:, :, 0] * 255))
    
            # TransmissionComposition(folder, transmission, number, param='refined_15_175_175')
            sceneRadiance_GB = sceneRadianceGB(img, transmission, AtomsphericLightRGB)
    
            # cv2.imwrite('OutputImages/' + prefix + 'GBDehazed.jpg', sceneRadiance_GB)
    
    
            # # print('sceneRadiance_GB',sceneRadiance_GB)
            sceneRadiance = sceneradiance(img, sceneRadiance_GB)
            # sceneRadiance= sceneRadiance_GB
            # cv2.imwrite('OutputImages/'+ prefix + 'GBDehazedRcoorectionUDCP.jpg', sceneRadiance)
            # # print('np.min(sceneRadiance)',np.min(sceneRadiance))
            # # print('sceneRadiance',sceneRadiance)
            
            S_x = AdaptiveExposureMap(img, sceneRadiance, Lambda=0.3, blockSize=blockSize)
            # print('S_x',S_x)
            sceneRadiance = AdaptiveSceneRadiance(sceneRadiance, S_x)
            
            
            if(int(tag)):
                h,w,c = sceneRadiance.shape 
             
                if (int(firstCall)):
                    cv2.putText(sceneRadiance, '_GBDehazedRcoorectionUDCPAdaptiveMap', (0,h-10) ,cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 2 )
                else:
                    cv2.putText(sceneRadiance, '_GBDehazedRcoorectionUDCPAdaptiveMap', (0,h-30) ,cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 2 )
            # print('sceneRadiance',sceneRadiance)
            cv2.imwrite(os.path.join(folder,'OutputImages',(prefix + '_GBDehazedRcoorectionUDCPAdaptiveMap.jpg')), sceneRadiance)


    
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


