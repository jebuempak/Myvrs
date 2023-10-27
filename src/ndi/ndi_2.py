import sys
import time
import numpy as np
import cv2 as cv
import NDIlib as ndi
from cvzone.SelfiSegmentationModule import SelfiSegmentation

def main():
    # NDI 초기화
    if not ndi.initialize():
        return 0

    # 영상 촬영 초기화
    cap = cv.VideoCapture(0)

    # NDI Send 설정
    send_settings = ndi.SendCreate()
    send_settings.ndi_name = 'ndi-python'
    ndi_send = ndi.send_create(send_settings)

    # NDI VideoFrame 설정
    video_frame = ndi.VideoFrameV2()

    # SelfiSegmentation 초기화
    segment = SelfiSegmentation()

    start = time.time()
    while time.time() - start < 60 * 5:
        start_send = time.time()

        for _ in reversed(range(200)):
            ret, img = cap.read()
            if ret:
                # 좌우 반전
                img = cv.flip(img, 1)

                # 배경 제거
                backOut = segment.removeBG(img, cutThreshold=0.1)

                # 알파 채널(투명도) 마스크 생성
                mask = (backOut != [0, 0, 0]).all(axis=2).astype(np.uint8) * 255

                # BGR + 알파 마스크 병합
                img_bgra = cv.merge((backOut, mask))

                # 화면에 배경 제거한 영상 출력
                cv.imshow('Transparent Background', img_bgra)

                # NDI 전송
                video_frame.data = img_bgra
                video_frame.FourCC = ndi.FOURCC_VIDEO_TYPE_BGRX
                ndi.send_send_video_v2(ndi_send, video_frame)

            # ESC 키를 누르면 종료
            key = cv.waitKey(1)
            if key == 27:
                cv.destroyAllWindows()
                ndi.send_destroy(ndi_send)
                ndi.destroy()
                return 0

        print('200 frames sent, at %1.2ffps' % (200.0 / (time.time() - start_send)))

    ndi.send_destroy(ndi_send)
    ndi.destroy()
    return 0

if __name__ == "__main__":
    sys.exit(main())
