# Underwater-Image-Processing
Test software for processing underwater images for the purpose of making text more readable. Heavily based on "An Experimental-based Review of Image
Enhancement and Image Restoration Methods for Underwater Imaging" [DOI 10.1109/ACCESS.2019.2932130, IEE Access]

Since the implementation is in test form, specific file structures are required. Once you have code on your device, the root repository should have 3 folders.

InputImages

OutputImages

SRC

The location of said repository doesn't matter, but these folders must exist. 
InputImages is where you save images that you want to process. 
OutputImages is folder where processed images are stored. 
Src is all the code for all the algorithms.

Main branch contains all algorithms, and main.py in the root of the SRC directory will run all input images through all algorithms, while the ProposedSolution branch will only run input images through CLACHE, HE and RGHS, as proposed in the report.



*******************************



Requires: 

python

cv2

numpy

scipy

matplotlib

scikit-image

natsort

math

datetime
