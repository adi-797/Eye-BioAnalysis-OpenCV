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

# Importing necessary libraries.
import cv2, imutils,pyrebase, numpy as np
from scipy.ndimage.interpolation import geometric_transform
def main():
    def topolar(img, order=5):
        max_radius = 0.5*np.linalg.norm( img.shape )
        def transform(coords):
            theta = 2.0*np.pi*coords[1] / (img.shape[1] - 1.)
            radius = max_radius * coords[0] / img.shape[0]
            i = 0.5*img.shape[0] - radius*np.sin(theta)
            j = radius*np.cos(theta) + 0.5*img.shape[1]
            return i,j

        polar = geometric_transform(img, transform, order=order,mode='nearest',prefilter=True)
        return polar
     
    """convert polar to cartesian"""
    def tocart(img, order=5):
        max_radius = 0.5*np.linalg.norm( img.shape )
        def transform(coords):
            xindex,yindex = coords
            x0, y0 = (255,255)
            x = xindex - x0
            y = yindex - y0
            r = np.sqrt(x ** 2.0 + y ** 2.0)*( img.shape[1]/max_radius)
            theta = np.arctan2(y, x,where=True)
            theta_index = (theta + np.pi) * img.shape[1] / (2 * np.pi)
            return (r,theta_index)
        polar = geometric_transform(img, transform, order=order,mode='nearest',prefilter=True)
        return polar

    def nothing(temp):
        pass

    # Reading image.
    img1 = cv2.imread('download1.jpg')
    img2 = img1
    blur = cv2.medianBlur(img2,5)
    bil = cv2.bilateralFilter(blur,5,1000,1000)
    copy_orig = bil.copy()
    gray = cv2.cvtColor(bil,cv2.COLOR_BGR2GRAY)
    ret,thresh1 = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)

    cv2.imshow('Masked Image', thresh1)

    # Trackbar for changing the threshold value.
    cv2.createTrackbar('min_value','Masked Image',0,255,nothing)

    # Trackbar execution.
    while(1):
        cv2.imshow('Masked Image', thresh1)
         
        min_value = cv2.getTrackbarPos('min_value', 'Masked Image')
        ret,thresh1 = cv2.threshold(gray,min_value,255,cv2.THRESH_BINARY_INV)
        
        # If ESC is pressed, execution breaks from the loop.
        k = cv2.waitKey(37)
        if k == 27:
            cv2.destroyAllWindows()
            break
            
    # Contour detection.
    _, contours, hierarchy = cv2.findContours(thresh1, 1, 2)
    cont = max(contours, key=cv2.contourArea)

    # Center and radius detection of pupil.
    (x,y), pupil_radius = cv2.minEnclosingCircle(cont)
    pupil_center = (int(x), int(y))
    pupil_radius = int(pupil_radius)
    cv2.circle(img2, pupil_center, pupil_radius, (0,0,255), 2)

    # Multiplier based on general ratio of radius of iris to pupil.
    iris_radius = pupil_radius*4

    # Radius detection for Iris.
    (cx,cy) = (int(x)+iris_radius, int(y))

    while(1):
        color = gray[cy,cx]
        if color>110:
            cx = cx-1
        else:
            break

    iris_radius = cx-pupil_center[0]
    cv2.circle(img2,pupil_center,iris_radius , (0,0,255), 2)

    # Output Image for detected pipil and iris.
    cv2.imshow('iris+pupil detection', img2)
    cv2.waitKey()
    cv2.destroyAllWindows()

    # Finding the minimum bounded rectangle.
    cv2.circle(img2,pupil_center,iris_radius , (255,255,255), -1)
    gray1 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
    ret,thresh2 = cv2.threshold(gray1,250,255,cv2.THRESH_BINARY)
    _, contours, hierarchy = cv2.findContours(thresh2, 1, 2)
    if len(contours)>0:
        maxC = max(contours, key=cv2.contourArea)
        x,y,w,h = cv2.boundingRect(maxC)
        cv2.rectangle(img2,(x,y),(x+w,y+h),(255,255,255),2)

    # Cropping to a standard size.
    cropped = copy_orig[y:y+h, x:x+w]
    cropped = cv2.resize(cropped, (240,240))

    mask = np.zeros(img2.shape, dtype = "uint8")
    cv2.circle(mask,pupil_center,iris_radius , (255,255,255), -1)
    cv2.circle(copy_orig, pupil_center, int(pupil_radius*2.2), (0,0,0), -1)
    mask = mask[y:y+h, x:x+w]
    mask = cv2.resize(mask, (240,240))
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    copy_orig = copy_orig[y:y+h, x:x+w]
    copy_orig = cv2.resize(copy_orig, (240,240))
    res = cv2.bitwise_and(copy_orig,copy_orig, mask = mask)

    ##res = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    ##imga = np.asarray(res,dtype=np.float64)
    ##pol = topolar(imga)
    # Output Image for nomarlized iris.
    ##cv2.imshow('Normalize', pol)

    y, x = res.shape[:2]
    total = 0
    mat = 0
    for i in range(x):
        for j in range(y):
            arr = res[j, i]
            if (abs(arr[0]-arr[1])<=10) and (abs(arr[1]-arr[2])<=10) and (abs(arr[2]-arr[1]) <= 10):
               mat+=1           
            total+=1

    ratio_of_grey = mat/total
    print ratio_of_grey, mat, total


    # Should be validated based on invasive medical analysis.
    if ratio_of_grey>= 0.2 and ratio_of_grey<= 0.35:
        print "MILD"
    elif ratio_of_grey> 0.35:
        print "HIGH"
    else:
        print "NORMAL"
    cv2.imwrite("8.jpg", res)
    cv2.imshow('Normalizegdfg', res)
    cv2.imshow('Normalized', cropped)
    cv2.waitKey()
    cv2.destroyAllWindows()

main()
