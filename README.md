# Stones_Morphology: Script developed in Python with OpenCV to detect the stones morphology.


Example of Input: 

![Muestra](https://github.com/Luisquii/Stones_Morphology/blob/master/imgs/Muestra5.jpeg)

(Or all the images in imgs folder)


After a Gausian Filter, Equalize, Contrast and Brightness modify, Adaptative treshold, Erode, Dilate and Find Contours, the result is the next:

![ContoursDetected](https://github.com/Luisquii/Stones_Morphology/blob/master/imgs/Morphology_ContoursDetected.png)


You can play with the Trackbars values:

The firstone is the Treshold Blocksize,
The secondone is the Contours min Size
The thirdone if it is Off you can Draw on the erode image to help the algorithm to detect or erase some stones, you draw with your right click and erase with yoyr left click,
if it is On, you can not draw

![Trackbars](https://github.com/Luisquii/Stones_Morphology/blob/master/imgs/TRackbars.png)

![Erode](https://github.com/Luisquii/Stones_Morphology/blob/master/imgs/Erode.png)
