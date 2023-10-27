import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_selfie_segmentation = mp.solutions.selfie_segmentation

# 모델 초기화
segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

# 웹캠 초기화
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    # 이미지를 RGB로 변환
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = segmentation.process(image_rgb)

    # Segmentation mask 얻기
    mask = results.segmentation_mask

    # 마스크 이진화
    _, thresholded_mask = cv2.threshold(mask, 0.5, 1, cv2.THRESH_BINARY)
    
    # 배경과 전경 분리
    fg_image = cv2.bitwise_and(frame, frame, mask=(thresholded_mask * 255).astype('uint8'))
    bg_mask = 1 - thresholded_mask
    bg_image = cv2.bitwise_and(frame, frame, mask=(bg_mask * 255).astype('uint8'))

    # 알파 채널(투명도)을 이용하여 배경을 투명하게 만듦
    alpha = (thresholded_mask * 255).astype('uint8')
    bgra = cv2.merge((fg_image[:, :, 0], fg_image[:, :, 1], fg_image[:, :, 2], alpha))

    # 결과 보기
    cv2.imshow('Sharp Selfie Segmentation', bgra)

    # ESC를 누르면 종료
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
