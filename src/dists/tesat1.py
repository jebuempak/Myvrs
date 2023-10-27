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

while True:
    ret, img = cap.read()
    
    if ret:
        # 좌우 반전
        img = cv2.flip(img, 1)

        # 배경 제거
        backOut = segment.removeBG(img, cutThreshold=0.1)

        # 알파 채널(투명도) 마스크 생성
        mask = (backOut != [0, 255, 0]).all(axis=2).astype(np.uint8) * 255

        # 초록색 배경 생성
        green_background = np.zeros_like(img, dtype=np.uint8)
        green_background[:, :] = [0, 255, 0]

        # 마스크를 이용하여 배경을 초록색으로 바꾸기
        green_image = cv2.bitwise_and(green_background, green_background, mask=255 - mask)
        final_output = cv2.add(backOut, green_image)

        # 화면에 초록색 배경이 추가된 영상 출력
        cv2.imshow('Green Screen Background', final_output)

        # NDI 전송 설정 및 전송
        video_frame = ndi.VideoFrameV2()
        video_frame.data = final_output
        video_frame.FourCC = ndi.FOURCC_VIDEO_TYPE_BGRX
        ndi.send_send_video_v2(ndi_send, video_frame)

        # ESC 키를 누르면 종료
        key = cv2.waitKey(20)
        if key == 27:
            break

cv2.destroyAllWindows()
ndi.send_destroy(ndi_send)
ndi.destroy()
