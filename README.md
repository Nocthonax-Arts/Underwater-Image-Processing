# Underwater-Image-Processing
Test software for processing underwater images for purpose of making text more readable. Heavily based on Underwater-Image-Enhancement-and-Color-Restoration paper

Since the implementation is in test form, specific file strucutre is required. 
Once you have code on you device, root reposistory should have 3 folders 

InputImages

OutputImages

SRC

Location of said repository doesen't matter, but these folders must exist. 
InputImages is where you put images you want processsed. 
OutputImages is folder where processed images are stored
And src is all the code for all the algorithms


Main branch contains all algorythms and main.py in root of SRC directory will run all input images through all algorythms
ProposedSolution branch will only run input images through CLACHE, HE and RGHS, as proposed in the report 



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
