import cv2
import tensorflow as tf

# 모델 로드 (여기서는 U-Net을 예로 들었지만, 실제 파일 경로 및 모델 구조에 따라 로드 과정이 다를 수 있음)
model = tf.keras.models.load_model('path_to_your_model.h5')

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, image = cap.read()
    if not ret:
        break

    # 모델에 맞게 이미지 전처리
    input_image = cv2.resize(image, (128, 128))  # 모델 입력 크기에 맞게 조정
    input_image = input_image / 255.0
    input_image = tf.expand_dims(input_image, axis=0)

    # 세그멘테이션 예측
    prediction = model.predict(input_image)
    mask = prediction.squeeze() > 0.5

    # 결과 마스크를 바탕으로 배경 제거
    mask_resized = cv2.resize(mask.astype('float32'), (image.shape[1], image.shape[0]))
    condition = mask_resized > 0.5
    background = [0, 0, 0]
    image[~condition] = background

    cv2.imshow('Segmented', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
