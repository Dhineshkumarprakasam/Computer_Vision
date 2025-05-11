import cv2

img = cv2.imread("birds.jpg")

#convert to gray scale
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

#threshold
ret, thresh = cv2.threshold(gray,150,255,cv2.THRESH_BINARY_INV)

contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    if cv2.contourArea(cnt) > 200:
        cv2.drawContours(img,cnt, -1,(0,0,255),2)
        x1, y1, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(img,(x1,y1),(x1+w,y1+h),(0,255,0),2)

cv2.imshow("frame",thresh)
cv2.imshow("org",img)

if cv2.waitKey(0) == ord("q"):
    exit()
