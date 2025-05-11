import cv2
import numpy as np
from PIL import Image

video = cv2.VideoCapture(0)

def get_limits(color):
    c = np.uint8([[color]])
    hsvc = cv2.cvtColor(c,cv2.COLOR_BGR2HSV)

    lowerLimit = hsvc[0][0][0] - 10,100,100
    upperLimit = hsvc[0][0][0] + 10,255,255

    ll = np.array(lowerLimit,dtype=np.uint8)
    ul = np.array(upperLimit,dtype=np.uint8)

    return ll,ul

ll,ul = get_limits([0,255,0]) #green color


while True:
    ret, frame = video.read()
    hsvImage = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsvImage,ll,ul)

    #getting bounding box
    mask_ = Image.fromarray(mask)
    bbox = mask_.getbbox()

    if bbox is not None:
        x1,y1,w,h = bbox
        frame = cv2.rectangle(frame,(x1,y1),(w,h),(0,0,255),5)

    cv2.imshow("frame",cv2.flip(frame,1))

    if cv2.waitKey(40) == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
