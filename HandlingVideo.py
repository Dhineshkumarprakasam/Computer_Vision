import cv2

#path
ip="video.mp4"

video = cv2.VideoCapture(ip)

#visualize video
ret = True
while ret:
    ret,frame=video.read()

    if ret:
        cv2.imshow('frame',frame)
        cv2.waitKey(40)

video.release()
cv2.destroyAllWindows()
