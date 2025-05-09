import cv2

img = cv2.imread('image.jpg')
print("Current size : ",img.shape)
cv2.imshow('frame',img)
cv2.waitKey(0)

#resize
new = cv2.resize(img,(600,400))
print("New size : ",new.shape)
cv2.imshow('frame2',new)
cv2.waitKey(0)

#crop
cropped = img[200:600,56:450]
cv2.imshow('cropped',cropped)
cv2.waitKey(0)

#save cropped image
cv2.imwrite('cropped.png',cropped)
