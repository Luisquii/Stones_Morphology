import cv2
import numpy as np
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.pyplot as plt
import time
def nothing(x):
    pass

def mouse_erasing(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Color: Black")
        print(x, y)
        # px = erode[y, x]
        # print(px)
        erode[y - 1, x] = 0 ; erode[y, x] = 0 ; erode[y + 1, x] = 0
        erode[y, x - 1] = 0; erode[y, x + 1] = 0
        erode[y + 1, x - 1] = 0; erode[y + 1, x + 1] = 0
        erode[y - 1, x - 1] = 0; erode[y - 1, x + 1] = 0
        erode[y - 2, x - 1] = 0; erode[y + 2, x - 1] = 0
        erode[y - 2, x] = 0; erode[y + 2, x] = 0
        erode[y - 2, x + 1] = 0; erode[y + 2, x + 1] = 0
    elif event == cv2.EVENT_RBUTTONDOWN:
        print("Color: White")
        # px = erode[y, x]
        # print(px)
        erode[y - 1, x] = 255; erode[y, x] = 255; erode[y + 1, x] = 255
        erode[y, x - 1] = 255; erode[y, x + 1] = 255
        erode[y + 1, x - 1] = 255; erode[y + 1, x + 1] = 255
        erode[y - 1, x - 1] = 255; erode[y - 1, x + 1] = 255
        erode[y - 2, x - 1] = 255; erode[y + 2, x - 1] = 255
        erode[y - 2, x] = 255; erode[y + 2, x] = 255
        erode[y - 2, x + 1] = 255; erode[y + 2, x + 1] = 255

kernel1 = np.ones((3,3), np.uint8)
kernel2 = np.ones((9,9), np.uint8)


img = cv2.imread("imgs/Muestra5.jpeg")
cv2.imshow("Input Image", img)
Gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


#Gausian Filter
gausfilter = cv2.GaussianBlur(img, (3,3), 0)


#Equalize Input Image
equalized = cv2.equalizeHist(Gray)
cv2.imshow("Gray-Equalized", equalized)

#Modify Contrast and Brightness
#alpha -> Contrast [1.0 to 3.0]
#Beta -> Brightness [0-100]
CandB = cv2.convertScaleAbs(equalized, alpha=1.1,beta=20)



#Create Trackbars
cv2.namedWindow("MorphoTrackbars",flags=0)
cv2.createTrackbar("Threshold BlockSize","MorphoTrackbars", 3, 5000, nothing)
cv2.createTrackbar("Contours min Size", "MorphoTrackbars", 1, 50, nothing)
cv2.createTrackbar("On/Off Erode", "MorphoTrackbars", 1, 1, nothing)
#Create Erode window ( Just for mouse event works)
cv2.namedWindow("Erode")
cv2.setMouseCallback("Erode", mouse_erasing)
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
    if cv2.getTrackbarPos("On/Off Erode", "MorphoTrackbars") == 1:
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

nMuestra = ("0",)
nArea = [0.0]
for i in range(0, len(copycontours),1):
    cnt = contours[i]
    area = cv2.contourArea(cnt)
    nMuestra = nMuestra +(str(i+1) ,)  #objects
    nArea.append(area)  #Performance
    print("area [" +str(i) +"] : " + str(area))


cv2.destroyAllWindows()

print nMuestra
print nArea
nArea.sort()
print nArea
y_pos = np.arange(len(nMuestra))
plt.bar(y_pos, nArea, align="center", alpha= 0.5)
plt.xticks(y_pos, nMuestra)
plt.ylabel("Area")
plt.title("Morphology")
plt.show()
