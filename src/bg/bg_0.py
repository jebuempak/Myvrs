import cv2
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import os

#카메라로 부터 영상촬영
cap = cv2.VideoCapture(0)

#세그멘테이션 class
segment = SelfiSegmentation()

#배경이미지
imgBG = cv2.imread("backimg1.png")

while True:
	#영상 촬영
	ret, img = cap.read()
	#좌우 반전
	img =  cv2.flip(img, 1)    
	#배경 삭제하고 이미지 넣기
	imgBG = cv2.resize(imgBG, (img.shape[1], img.shape[0]))

	backOut = segment.removeBG(img, imgBG, cutThreshold=0.1 )
	#이미지 보여주기
	#cv2.imshow("CAM", img)
	cv2.imshow('back remove', backOut)
	# esc 키 누르면 빠져 나오기
	key = cv2.waitKey(20)
	if key == 27:
		break

cv2.destroyAllWindows
