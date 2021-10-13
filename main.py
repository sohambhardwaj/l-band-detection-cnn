from typing import Sized
import cv2
import numpy as np
from PIL import Image

def getContour(img,imgCont) :
    contours, hierarchy=cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(imgCont,contours,-1,(255,0,255),5)
    # print(len(contours))
    # for cnt in contours:
    #     area=cv2.contourArea(cnt)
    #     if(area<5000):
    #         cv2.drawContours(imgCont,contours,-1,(255,0,255),2)


while(True):
    img=cv2.imread('example.jpg')
    height = img.shape[0]
    width = img.shape[1]
    # img=cv2.rectangle(img,(5,5),(width-5,height-5),(0, 0, 0),10)

    img=cv2.line(img, (0, 0), (0, height), (255, 255, 255), thickness=15)
    img=cv2.line(img, (width, 0), (width, height), (255, 255, 255), thickness=15)
    imgCont=img.copy()
    imgBlur=cv2.GaussianBlur(img,(11,11),1)
    imgGray=cv2.cvtColor(imgBlur,cv2.COLOR_BGR2GRAY)
    imgCanny=cv2.Canny(imgGray,50,50)
    kernel=np.ones((3,3))
    imgDil=cv2.dilate(imgCanny,kernel,iterations=1)
    getContour(imgDil,imgCont)
    cv2.imshow("result",imgCont)
    if(cv2.waitKey(1) & 0xFF ==ord('q')):
        break
cv2.destroyAllWindows()
