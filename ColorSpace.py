import cv2

img = cv2.imread('image.jpg')
cv2.imshow('image',img)


#swap color
swapped = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
cv2.imshow('RGB to BGR',swapped)

#convert image to gray scale
gray = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
cv2.imshow('Gray scale',gray)

#convert to hsv
hsv = cv2.cvtColor(img,cv2.COLOR_RGB2HSV)
cv2.imshow('HSV',hsv)

cv2.waitKey(0)
