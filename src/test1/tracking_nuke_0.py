import cv2
import mediapipe as mp
import numpy as np

mp_selfie_segmentation = mp.solutions.selfie_segmentation

# MediaPipe 세그멘테이션 모델 초기화
segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=0)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, image = cap.read()
    if not ret:
        break

    # RGB 이미지로 변환
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    
    # 세그멘테이션 수행
    result = segmentation.process(image_rgb)

    # 배경과 전경 분리
    condition = result.segmentation_mask > 0.5  # 마스크 생성
    background = 0  # 배경을 검은색으로
    image[np.logical_not(condition)] = background

    cv2.imshow('Background Removed', image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
