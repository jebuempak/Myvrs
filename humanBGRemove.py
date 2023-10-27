import sys
import time
import numpy as np
import cv2 as cv
import NDIlib as ndi
import mediapipe as mp

mp_selfie_segmentation = mp.solutions.selfie_segmentation
segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=0)

def main():
	if not ndi.initialize():
		return 0

	cap = cv.VideoCapture(0)
	send_settings = ndi.SendCreate()
	send_settings.ndi_name = 'ndi-python'

	ndi_send = ndi.send_create(send_settings)
	video_frame = ndi.VideoFrameV2()

	start = time.time()
	while time.time() - start < 60 * 5:
		try:
			print( time.time(), (time.time() - start < 60 * 5 ) )
			start_send = time.time()

			#for _ in reversed(range(200)):
			ret, img = cap.read()
			if ret:
				# RGB 이미지로 변환
				image_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)

				# 세그멘테이션 수행
				result = segmentation.process(image_rgb)

				# 배경과 전경 분리
				condition = result.segmentation_mask > 0.5  # 마스크 생성
				img_bgra = cv.cvtColor(img, cv.COLOR_BGR2BGRA)
				img_bgra[np.logical_not(condition)] = [0, 255, 0, 255]  # 배경을 알파레이어로

				video_frame.data = img_bgra
				video_frame.FourCC = ndi.FOURCC_VIDEO_TYPE_BGRX
				ndi.send_send_video_v2(ndi_send, video_frame)
		except:
			pass

		print('200 frames sent, at %1.2ffps' % (200.0 / (time.time() - start_send)))
	

	ndi.send_destroy(ndi_send)
	ndi.destroy()

	return 0

if __name__ == "__main__":
	sys.exit(main())
