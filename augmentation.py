import cv2 as cv
import numpy as np
from numpy import random
from scipy.io import loadmat


def removePatches(image,position,patch_size,color):
	des=image.copy()
	h=patch_size[0]//2
	w=patch_size[1]//2	
	x=position[0]
	y=position[1]
	
	for i in range(x-h,x+h):
		for j in range(y-w,y+w):
			if color==1:
				des[i][j]=[255,255,255]	
			else:
				des[i][j]=[0,0,0]			
	return des

def getPosition(h,w,patch_h,patch_w):
	x=np.random.randint(patch_h,h-patch_h-1)
	y=np.random.randint(patch_w,w-patch_w-1)
	return x,y

def RandomPatches(image,patch_size,position,color=1):
	[h,w,c]=image.shape
	des_img=image.copy()
	
	patch_h=patch_size[0]
	patch_w=patch_size[1]
	x,y=position
		
	des_img=removePatches(des_img,(x,y),patch_size,color)
	return des_img

def RotatePoint(point,theta):
	R=np.array([[np.cos(theta),np.sin(theta),0],
				[-np.sin(theta),np.cos(theta),0],
				[0,0,1]])

	Rpoint=[point[0],point[1],1]
	new_point=R@Rpoint
	return (new_point[0],new_point[1])
	
def getNewPose(vertices,coor,theta1,theta2,theta3):
	X0=np.ones((vertices.shape[0],1))
	ver=np.hstack((vertices,X0))
	x,y,w,h=coor[0],coor[1],coor[2],coor[3]

	Rx=np.array([[1,0,0,0],
				[0,np.cos(theta1),np.sin(theta1),0],
				[0,-np.sin(theta1),np.cos(theta1),0],
				[0,0,0,1]])

	Ry=np.array([[np.cos(theta2),0,-np.sin(theta2),0],
				[0,1,0,0],
				[np.sin(theta2),0,np.cos(theta2),0],
				[0,0,0,1]])

	Rz=np.array([[np.cos(theta3),np.sin(theta3),0,0],
				[-np.sin(theta3),np.cos(theta3),0,0],
				[0,0,1,0],
				[0,0,0,1]])
	R=Rz@Ry@Rx
	new_pose=ver@R

	left=np.min(new_pose[:,0])
	right=np.max(new_pose[:,0])
	top=np.min(new_pose[:,1])
	bottom=np.max(new_pose[:,1])
	
	center=np.array([right - (right - left) / 2.0, bottom - (bottom - top) / 2.0])
	dx=(right - left)/2
	dy=(bottom - top)/2
	d=np.max([dx,dy])

	x=center[0]-d
	w=center[0]+d
	y=center[1]-d
	h=center[1]+d

	new_c=(int(x),int(y),int(w),int(h))	
	return new_pose[:,:3],new_c
	
def getAngles():
	theta1=np.random.randint(-10,10)
	theta2=np.random.randint(-10,10)
	theta3=np.random.randint(-10,10)
	
	t1=np.pi*theta1/180
	t2=np.pi*theta2/180
	t3=np.pi*theta3/180

	return t1,t2,t3

def blurImage(image,sigma,kernel):
	aug_img=cv.GaussianBlur(image,(5,5),10)
	return aug_img

def constract(img,c=3.0,k_szie=3):
	clahe = cv.createCLAHE(clipLimit=c, tileGridSize=(k_size,k_size))
	lab = cv.cvtColor(img, cv.COLOR_BGR2LAB) 
	l, a, b = cv.split(lab)  
	l2 = clahe.apply(l)  
	lab = cv.merge((l2,a,b)) 
	img2 = cv.cvtColor(lab, cv.COLOR_LAB2BGR)
	return img2

