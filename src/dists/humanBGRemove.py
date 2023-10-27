import cv2
import numpy as np
import NDIlib as ndi
from cvzone.SelfiSegmentationModule import SelfiSegmentation

# NDI 초기화
if not ndi.initialize():
    exit(0)

# 영상 촬영 초기화
cap = cv2.VideoCapture(0)

# NDI Send 설정
send_settings = ndi.SendCreate()
send_settings.ndi_name = 'ndi-python'
ndi_send = ndi.send_create(send_settings)

# SelfiSegmentation 초기화
segment = SelfiSegmentation()

# 배경 이미지
imgBG = cv2.imread("2023-10-22-20-27-14.png", cv2.IMREAD_UNCHANGED)

# 알파 채널 제거
imgBG = imgBG[:, :, :3]

while True:
    ret, img = cap.read()
    
    if ret:
        # 좌우 반전
        img = cv2.flip(img, 1)
        imgBG = cv2.resize(imgBG, (img.shape[1], img.shape[0]))

        # 배경 제거
        backOut = segment.removeBG(img, imgBG, cutThreshold=0.1)

        # 알파 채널(투명도) 마스크 생성
        mask = (backOut != [0, 0, 0]).all(axis=2).astype(np.uint8) * 255

        # BGR + 알파 마스크 병합
        img_bgra = cv2.merge((backOut, mask))

        # 화면에 배경 제거한 영상 출력
        cv2.imshow('Transparent Background', img_bgra)

        # NDI 전송 설정 및 전송
        video_frame = ndi.VideoFrameV2()
        video_frame.data = img_bgra
        video_frame.FourCC = ndi.FOURCC_VIDEO_TYPE_BGRX
        ndi.send_send_video_v2(ndi_send, video_frame)

        # ESC 키를 누르면 종료
        key = cv2.waitKey(20)
        if key == 27:
            break

cv2.destroyAllWindows()
ndi.send_destroy(ndi_send)
ndi.destroy()
