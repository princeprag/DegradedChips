import cv2
import numpy as np
img=cv2.imread('sample.png')
imgc=cv2.imread('sample.png')
img2=cv2.imread('sample.png')
cv2.imshow('originalImage',img2)

roi=[]
areaChips=[]
areasumRed=[]

img_hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
img_gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)





#HSV SLIDER TO FIND RANGE OF RAW MATERIAL
def nothing(x):
	pass

def filter():
	cv2.namedWindow('HSV')
	cv2.createTrackbar('low_H', 'HSV', 0, 255, nothing)
	cv2.createTrackbar('low_S', 'HSV', 0, 255, nothing)
	cv2.createTrackbar('low_V', 'HSV', 0, 255, nothing)
	cv2.createTrackbar('high_H', 'HSV', 255, 255, nothing)
	cv2.createTrackbar('high_S', 'HSV', 255, 255, nothing)
	cv2.createTrackbar('high_V', 'HSV', 255, 255, nothing)
	
	while(True):
		hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		low_H = cv2.getTrackbarPos('low_H', 'HSV')
		low_S = cv2.getTrackbarPos('low_S', 'HSV')
		low_V = cv2.getTrackbarPos('low_V', 'HSV')
		high_H = cv2.getTrackbarPos('high_H', 'HSV')
		high_S = cv2.getTrackbarPos('high_S', 'HSV')
		high_V = cv2.getTrackbarPos('high_V', 'HSV')
		low_limit = np.array([low_H,low_S,low_V])
		high_limit = np.array([high_H,high_S,high_V])
		mask = cv2.inRange(hsv, low_limit, high_limit)
		cv2.imshow('frame',img)
		cv2.imshow('mask', mask)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	cv2.destroyAllWindows()


#Range for WHITE colour
l=np.array([5,110,50],np.uint8)
u=np.array([255,255,255],np.uint8)
mask=cv2.inRange(img_hsv,l,u)
#cv2.imshow('mask',mask)
white=cv2.bitwise_and(img,img,mask=mask)

#blurring using median blurr
b1=cv2.medianBlur(mask,5)

# Applying EROSION & DILATION TO SEPERATE THE CLOSED CHIPS
kernel=np.ones((15,15),np.uint8)
erosion=cv2.erode(b1,kernel,iterations=1)

kernel2=np.ones((15,15),np.uint8)
dilation=cv2.dilate(erosion,kernel2,iterations=1)


#Finding CONTOURS for chips
cnt,hierarchy=cv2.findContours(dilation,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img,cnt,-1,(255,0,0),2)
cv2.imshow('cntr',img)
print(len(cnt))

#range for red colour
l1=np.array([0,175,105],np.uint8)
u1=np.array([20,255,255],np.uint8)
masu=cv2.inRange(img_hsv,l1,u1)
orang=cv2.bitwise_and(imgc,imgc,mask=masu)
#creating mask & finding only Red AREA



#range for green-brown colour
lg=np.array([22,80,40],np.uint8)
ug=np.array([25,255,255],np.uint8)


#Now,using for loop to find area of each chips,storing it in a list

for i in range (0,24):
	font=cv2.FONT_HERSHEY_SIMPLEX
	area=cv2.contourArea(cnt[i])
	areaChips.append(area)
	#creating rectangle
	x,y,w,h=cv2.boundingRect(cnt[i])
	cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),1)
	cv2.rectangle(orang,(x,y),(x+w,y+h),(255,0,0),1)
	# Putting text as numbers
	#cv2.putText(img,str(i+1),(x,y),font,1,(0,0,255),1,cv2.LINE_AA)
	#finding roi for each image
	r=img[y:y+h,x:x+w]
	roi.append(r) 
	cv2.imwrite('roi'+str(i+1)+'.jpg',r)
	#finding the red region in each region of intrest individually
	img_hsvr=cv2.cvtColor(r,cv2.COLOR_BGR2HSV)
	maskk=cv2.inRange(img_hsvr,l1,u1)
	orangeee=cv2.bitwise_and(r,r,mask=maskk)
	#finding contours for red
	cntt,hierarchy=cv2.findContours(maskk,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(orangeee,cntt,-1,(255,0,0),0)
	l=len(cntt)
	#finding contours for green-brown
	maskg=cv2.inRange(img_hsvr,lg,ug)
	green=cv2.bitwise_and(r,r,mask=maskg)
	cntg,hierarchy=cv2.findContours(maskg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	cv2.drawContours(green,cntg,-1,(255,0,0),0)
	k=len(cntg)
	#print(l)
	summ=0
	summm=0
	#since we have many small contours scattered through the whole area of chips finding the total area by first finding total no of contours & then summation using for loop
	# REMEMBER we are doing this for each chips individually  
	for j in range (0,l):
		ara=cv2.contourArea(cntt[j])
		summ=summ+ara
	areasumRed.append(summ)
	div= areasumRed[i]/areaChips[i]
	#checking for threshold value and printing *** to chips rejected
	if div > 0.68:
		cv2.putText(img,'***',(x,y),font,1,(0,0,255),1,cv2.LINE_AA)
	#checking for trace of any other colour and printing *** to chips rejected
	for t in range (0,k):
		araa=cv2.contourArea(cntg[t])
		summm=summm+araa
	if summm > 0:
		cv2.putText(img,'***',(x,y),font,1,(0,0,255),1,cv2.LINE_AA)

#showing the final result
cv2.imshow('orang',orang)
cv2.imshow('finalResult',img)	



cv2.waitKey(0)
cv2.destroyAllWindows()







