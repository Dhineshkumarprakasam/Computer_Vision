import cv2

#read
webcam = cv2.VideoCapture(0)

#visualize
while True:
    ret, frame = webcam.read()
    cv2.imshow("frame",cv2.flip(frame,1))
    
    if cv2.waitKey(40) == ord('q'):
        break
        
webcam.release()
cv2.destroyAllWindows()
