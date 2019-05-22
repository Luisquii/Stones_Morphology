import cv2
import numpy as np


def nothing(x):
    pass

kernel1 = np.ones((3,3), np.uint8)
kernel2 = np.ones((9,9), np.uint8)


img = cv2.imread("Muestra1.png")
cv2.imshow("Input Image", img)
Gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


#Gausian Filter
gausfilter = cv2.GaussianBlur(img, (3,3), 0 )



#Equalize Input Image
graygaus = cv2.cvtColor(gausfilter, cv2.COLOR_BGR2GRAY)
equalized = cv2.equalizeHist(Gray)


#Modify Contrast and Brightness
#alpha -> Contrast [1.0 to 3.0]
#Beta -> Brightness [0-100]
CandB = cv2.convertScaleAbs(equalized, alpha=1.1,beta=20)
cv2.imshow("Equalized", equalized)


#Create Trackbars
cv2.namedWindow("MorphoTrackbars")
cv2.createTrackbar("Threshold BlockSize","MorphoTrackbars", 3, 1023, nothing)
cv2.createTrackbar("Contours min Size", "MorphoTrackbars", 1, 50, nothing)


while(1):

    TEblockSize = cv2.getTrackbarPos("Threshold BlockSize","MorphoTrackbars")
    ContoursMinSize = cv2.getTrackbarPos("Contours min Size", "MorphoTrackbars")
    if TEblockSize == 0:
        TEblockSize = 3
    else:
        count = TEblockSize % 2
        if count == 0:
            TEblockSize = TEblockSize + 1
        else:
            TEblockSize = TEblockSize



    #Adaptative Threshold
    threshequalized = cv2.adaptiveThreshold(CandB, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, TEblockSize, 5)
    cv2.imshow("TreshEqualized33", threshequalized)

    #Erode
    erode = cv2.erode(threshequalized, kernel1, iterations=1)
    erode = cv2.erode(erode, kernel2, iterations=1)
    cv2.imshow("Erode", erode)

    #Dilate
    dilate = cv2.dilate(erode, kernel1, iterations=2)
    cv2.imshow("Dilate", dilate)

    #Find Contours
    imgcopy = img.copy()
    image, contours, hierarchy = cv2.findContours(dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    lencontours = len(contours)
    copycontours = []
    for i in range(0,lencontours,1):
        lenofcontourspos = len(contours[i])
        if lenofcontourspos >= ContoursMinSize:
            copycontours.append(contours[i])

    drawContours = cv2.drawContours(imgcopy, copycontours, -1, (0,255,0), 2, maxLevel=1)
    cv2.imshow("Contours", drawContours)


    k = cv2.waitKey(1) & 0xFF
    if k == 32:
        break

for i in range(0, len(copycontours),1):
    cnt = contours[i]
    area = cv2.contourArea(cnt)
    print("area [" +str(i) +"] : " + str(area))

cv2.destroyAllWindows()