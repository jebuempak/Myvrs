import cv2
import cvzone
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import numpy as np

# 카메라로 부터 영상촬영
cap = cv2.VideoCapture(0)

# 세그멘테이션 class
segment = SelfiSegmentation()

while True:
    # 영상 촬영
    ret, img = cap.read()
    if not ret:
        break

    # 좌우 반전
    img = cv2.flip(img, 1)

    # 배경 삭제하고 이미지 넣기
    backOut = segment.removeBG(img, cutThreshold=0.1)

    # 알파 채널(투명도)을 위한 마스크 생성
    mask = (backOut != [0, 0, 0]).all(axis=2).astype(np.uint8) * 0
    img_bgra = cv2.merge((img, mask))

    # 이미지 보여주기
    cv2.imshow('back remove', backOut)  # 여기서는 원본 이미지와 동일한 이미지를 보여줍니다.

    # esc 키 누르면 빠져 나오기
    key = cv2.waitKey(20)
    if key == 27:
        break
    # s 키를 누르면 이미지 저장
    elif key == ord('s'):
        cv2.imwrite('transparent_image.png', img_bgra)  # PNG로 저장

cv2.destroyAllWindows()

