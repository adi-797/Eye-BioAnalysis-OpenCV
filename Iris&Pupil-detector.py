'''
Name : Aditya Arora
Dated : 10/8/2018
Affiliation : Bharati Vidyapeeth's College of Engineering, New Delhi - 63

MIT License

Copyright (c) 2018 Aditya Arora

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import cv2, imutils, numpy as np

def nothing(temp):
    pass

img1 = cv2.imread('download3.jpg')
img2=cv2.resize(img1, (640,480))
blur = cv2.medianBlur(img2,5)
img = cv2.bilateralFilter(blur,5,1000,1000)
cimg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,thresh1 = cv2.threshold(cimg,127,255,cv2.THRESH_BINARY_INV)

cv2.imshow('Masked Image', thresh1)
 
cv2.createTrackbar('min_value','Masked Image',0,255,nothing)
 
while(1):
    
    cv2.imshow('Masked Image', thresh1)
     
    min_value = cv2.getTrackbarPos('min_value', 'Masked Image')
    ret,thresh1 = cv2.threshold(cimg,min_value,255,cv2.THRESH_BINARY_INV)
     
    k = cv2.waitKey(37)
    if k == 27:
        cv2.destroyAllWindows()
        break
                                                                                             #creating a threshold for finding contours
_, contours, hierarchy = cv2.findContours(thresh1, 1, 2)
cont = max(contours, key=cv2.contourArea)

(x,y),radius = cv2.minEnclosingCircle(cont)
center = (int(x), int(y))
radius = int(radius)
cv2.circle(img2,center, radius, (0,0,255), 2)

iris_radius = radius*4

(cx,cy) = (int(x)+iris_radius, int(y))

while(1):
    color = cimg[cy,cx]
    if color>110:
        cx = cx-1
    else:
        break
    s
rad = cx-center[0]
cv2.circle(img2,center,rad , (0,0,255), 2)
cv2.imshow('iris+pupil detection', img2)
cv2.waitKey()
cv2.destroyAllWindows()
