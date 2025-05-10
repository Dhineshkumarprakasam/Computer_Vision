import cv2

img = cv2.imread('profile.jpg')

#resize
org=cv2.resize(img,(500,500))
cv2.imshow('orginal',org)
print("Before : ",img.shape," After : ",org.shape)

# blur
k_size = 101
blur1=cv2.blur(org,(k_size,k_size))
cv2.imshow('blured',blur1)

# Gaussian blur
blur2=cv2.GaussianBlur(org,(k_size,k_size),5)
cv2.imshow('gaussian blur',blur2)

# Median blur
blur3=cv2.medianBlur(org,k_size)
cv2.imshow('median blur',blur3)

cv2.waitKey(0)
