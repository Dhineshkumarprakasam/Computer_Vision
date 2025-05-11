import cv2

img = cv2.imread("border.jpg")
print("Shape : ",img.shape)

#lines
cv2.line(img,(200,100),(450,100),(0,255,0),3)
cv2.line(img,(200,150),(450,150),(255,0,0),3)
cv2.line(img,(200,200),(450,200),(0,0,255),3)
cv2.line(img,(200,250),(450,250),(0,0,0),3)

img2 = cv2.imread("border.jpg")

#rectangle
cv2.rectangle(img2,(120,80),(510,280),(0,0,0),-1)
cv2.rectangle(img2,(120,80),(510,280),(0,250,250),10)
cv2.rectangle(img2,(150,125),(250,225),(255,0,0),-1) #-1 for filling
cv2.rectangle(img2,(260,125),(360,225),(0,0,255),-1)
cv2.rectangle(img2,(370,125),(470,225),(0,255,0),-1)

#circle
cv2.circle(img2,(200,175),40,(255,255,255),-1)
cv2.circle(img2,(310,175),40,(255,255,0),15)
cv2.circle(img2,(420,175),40,(255,255,255),-1)

#text
cv2.putText(img2,"Dhinesh kumar",(200,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2)

cv2.imshow("frame1",img)
cv2.imshow("frame2",img2)

if cv2.waitKey(0) == ord('q'):
    exit()
