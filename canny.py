import cv2
import numpy as np
import imutils
from scipy.ndimage import rotate
from matplotlib import pyplot as plt


img = cv2.imread('scull.jpg',0)# read the X ray image in gray scale
edges = cv2.Canny(img,100,200) # apply Canny filter to loded image

height = np.size(img, 0)# get height of the image
width = np.size(img, 1)# get width of the image

###################################################################
def findExtRight(edges):# find Right extream point from the canny filtered image
	extRigth_x = 0
	extRigth_y = 0
	rotate_img = rotate(edges, 90)
	for a in range(35,width-1): # some X ray has scall in right top corner  between  0-35 pixel
		for b in range(1,height-1):
			if rotate_img[a][b] == 255:
				extRigth_x = a
				extRigth_y = b
				break
		if extRigth_x !=0 or extRigth_y !=0:
			break
	point_3_x = extRigth_y
	point_3_y = width - extRigth_x

	return point_3_x, point_3_y
#############################################
def findExLeft(edges):# find left extream point from the canny filtered image 
	extLeft_x = 0
	extLeft_y = 0
	rotate_img = rotate(edges, 270)
	for a in range(1 ,width-1):
		for b in range(1,height-1):
			if rotate_img[a][b] == 255:
				extLeft_x = a
				extLeft_y = b
				break
		if extLeft_x !=0 or extLeft_y !=0:
			break
	# print('new')
	# print(extLeft_x, extLeft_y)

	point_2_x = height-extLeft_y
	point_2_y = extLeft_x

	return point_2_x, point_2_y

#############################################
x_1, y_1 = findExLeft(edges)# call the findExtLeft function to get left extream point
x_2, y_2 = findExtRight(edges)# call the findExtLeft function to get Right extream point
#############################################
y = int(y_1 +(y_2 - y_1)/2) # pogonian X coordinate  of the skul is placed above exacty between extream right point and extream left point

k = 0
for i in range(1,height):# to find pogonian Y coodinate go top to buttom throught Y (IN ABOVE MENTION*******) 
	if img[i][y] > 250:
		k = i
		break

cv2.circle(edges,(y, k), 5, (255,255,255), -1)##draw the cricle on the skul and on the POG point
#############################################

test_point = y_2

return_point_x = 0
return_point_y = 0

for i in range(x_2, height-1):
	for j in range(test_point-3, test_point+3):
		if edges[i+1][j] == 255:
			test_point = j
			print(j)
			break
			
		if j == test_point + 3 and edges[i+1][j] == 0:
			return_point_y = j-3
			return_point_x = i-1
			break

	if return_point_x != 0:
		break


cv2.circle(edges,(return_point_y, return_point_x), 5, (255,255,255), -1)

cv2.imshow('img',edges )# show canny filtered image
cv2.imshow('img_1',img )# show input image (X ray image)
# cv2.imshow('scull image',edges)
# cv2.imshow('scull image_rotate',rotate_img)
cv2.waitKey(0)
cv2.destroyAllWindows() # wait until some key is press.....
# THE END

