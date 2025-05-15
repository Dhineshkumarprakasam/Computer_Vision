import cv2
import mediapipe as mp

def face_blur(img):
    face_detector = mp.solutions.face_detection
    with face_detector.FaceDetection(0.5,0) as detection:
        img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        out = detection.process(img_rgb)

        if out.detections!=None:
            for dd in out.detections:
                location_data = dd.location_data
                bbox = location_data.relative_bounding_box

                x1 = int(bbox.xmin * img.shape[1])
                y1 = int(bbox.ymin * img.shape[0])-30
                w = int(bbox.width * img.shape[1])+10
                h = int(bbox.height * img.shape[0])+20

                #blur
                img[y1:y1+h,x1:x1+w,:] = cv2.blur(img[y1:y1+h,x1:x1+w,:],(50,50))

        return img


video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()
    frame = cv2.flip(frame,1)
    img = face_blur(frame)
    cv2.imshow("Video",img)
    if cv2.waitKey(40) == ord('q'):
        break
