import cv2

video = cv2.VideoCapture(0)

while True:
    ret, img = video.read()

    img = cv2.flip(img,1)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    thresh2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 1)
    blur = cv2.medianBlur(thresh2, 3)

    cv2.imshow("frame",blur)
    cv2.imshow("frame2",img)
    if cv2.waitKey(40) == 27:
        break

video.release()
cv2.destroyAllWindows()
