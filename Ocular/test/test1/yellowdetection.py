import cv2, imutils, numpy as np

# cap = cv2.VideoCapture(1)

# while True:
#     ret, image = cap.read()
#     image = imutils.resize(image, width=640, height=480)
#     cv2.imshow("gray", image)
#     if cv2.waitKey(30)==27 & 0xff:
#                 ret, image = cap.read()
#                 break

# cap.release()
# cv2.destroyAllWindows()
image = cv2.imread('img_path')
copy = image.copy()
image = imutils.resize(image, width=640, height=480)
image = cv2.medianBlur(image,5)
image = cv2.bilateralFilter(image,5,1000,1000)
frame = image.copy()

hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
lower_yellow = np.array([19,45,120]) #all shades of yellow
upper_yellow = np.array([60,255,255])
mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
res = cv2.bitwise_and(frame,frame, mask = mask)
image = res.copy()
res = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
y, x = res.shape[:2]
total = 0
mat = 0
for i in range(x):
    for j in range(y):
        arr = res[j, i]
        if arr == 0:
            continue
        mat+=1
        total+=arr

print (mat, total)

average = float(total)/float(mat) #per pixel intensity
average = 1- np.interp(average, [0,255], [0,1])
print (average)
print ((average*mat)/61440)
cv2.imshow("gray", copy)
cv2.imshow("masked", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

