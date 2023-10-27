import cv2
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import numpy as np

# 카메라로부터 영상 촬영
cap = cv2.VideoCapture(0)

# 세그멘테이션 class
segment = SelfiSegmentation()

# 배경 이미지
imgBG = cv2.imread("Green.png")

while True:
    # 영상 촬영
    ret, img = cap.read()
    # 좌우 반전
    img = cv2.flip(img, 1)
    # 배경 이미지 크기 조절
    imgBG = cv2.resize(imgBG, (img.shape[1], img.shape[0]))

    # 배경 제거
    backOut = segment.removeBG(img, imgBG, cutThreshold=0.1)

    # 알파 채널(투명도) 마스크 생성
    mask = (backOut != [0, 0, 0]).all(axis=2).astype(np.uint8) * 255

    # BGR + 알파 마스크 병합
    img_bgra = cv2.merge((backOut, mask))

    # 투명한 이미지 출력
    cv2.imshow('Transparent Background', img_bgra)

    # esc 키 누르면 종료
    key = cv2.waitKey(20)
    if key == 27:
        break

cv2.destroyAllWindows()
