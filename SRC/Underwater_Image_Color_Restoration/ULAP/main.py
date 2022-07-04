import os
import sys
import datetime
import numpy as np
import cv2
import natsort

from GuidedFilter import GuidedFilter
from backgroundLight import BLEstimation
from depthMapEstimation import depthMap
from depthMin import minDepth
from getRGBTransmission import getRGBTransmissionESt
from global_Stretching import global_stretching
from refinedTransmissionMap import refinedtransmissionMap

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

            blockSize = 9
            gimfiltR = 50  
            eps = 10 ** -3  
    
            DepthMap = depthMap(img)
            DepthMap = global_stretching(DepthMap)
            guided_filter = GuidedFilter(img, gimfiltR, eps)
            refineDR = guided_filter.filter(DepthMap)
            refineDR = np.clip(refineDR, 0,1)
    
            #cv2.imwrite(os.path.join(folder,'OutputImages',(prefix + '_ULAPDepthMap.jpg')), np.uint8(refineDR * 255))
    
            AtomsphericLight = BLEstimation(img, DepthMap) * 255
    
            d_0 = minDepth(img, AtomsphericLight)
            d_f = 8 * (DepthMap + d_0)
            transmissionB, transmissionG, transmissionR = getRGBTransmissionESt(d_f)
    
            transmission = refinedtransmissionMap(transmissionB, transmissionG, transmissionR, img)
            sceneRadiance = sceneRadianceRGB(img, transmission, AtomsphericLight)

            #cv2.imwrite(os.path.join(folder,'OutputImages',(prefix + '_ULAP_TM.jpg')), np.uint8(transmission[:, :, 2] * 255))
    
            if(int(tag)):
                h,w,c = sceneRadiance.shape 
             
                if (int(firstCall)):
                    cv2.putText(sceneRadiance, '_ULAP', (0,h-10) ,cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 2 )
                else:
                    cv2.putText(sceneRadiance, '_ULAP', (0,h-30) ,cv2.FONT_HERSHEY_TRIPLEX, 0.5, (255, 255, 255), 2 )
    
            
            cv2.imwrite(os.path.join(folder,'OutputImages',(prefix + '_ULAP.jpg')), sceneRadiance)


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


