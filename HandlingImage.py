import cv2

#path
ip = "image.jpg"

#read
image = cv2.imread(ip)

#write with changing the image type
cv2.imwrite("hello.png",image)

#visualize
cv2.imshow("frame",image)
cv2.waitKey(0)
