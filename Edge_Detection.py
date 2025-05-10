import cv2
import numpy as np

img = cv2.imread("car.jpg")

#remove noise
img = cv2.medianBlur(img,1)

#edge thin
edge1 = cv2.Canny(img,250,500)

#increase the edge thickness
edge2 = cv2.dilate(edge1,np.ones((5,5),dtype=np.int8))

#decrease the edge thickness
edge3 = cv2.erode(edge2,cv2.dilate(edge1,np.ones((5,5),dtype=np.int8)))

cv2.imshow("edge",edge1)
cv2.imshow("dilate",edge2)
cv2.imshow("erode",edge3)
cv2.imshow("orginal",img)

cv2.waitKey(0)
