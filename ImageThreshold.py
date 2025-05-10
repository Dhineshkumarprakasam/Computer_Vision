import cv2

img = cv2.imread("profile.jpg")
img = cv2.resize(img,(500,500))

#gray scale
gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

#thresh
ret1,thresh1=cv2.threshold(gray,120,255,cv2.THRESH_BINARY)
cv2.imshow("normal thresh",thresh1)

#adaptive threshold
thresh2 = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,5)
cv2.imshow("adaptive threshold",thresh2)

#blur - removing noise
blur = cv2.medianBlur(thresh2,3)
cv2.imshow("adaptive threshold + median blured",blur)

cv2.waitKey(0)
