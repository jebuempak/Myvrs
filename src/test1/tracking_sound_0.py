import cv2
import mediapipe as mp
import pygame

# mediapipe 초기화
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands()

# pygame 초기화 (사운드 재생을 위해)
pygame.init()

# 사운드 로드
sound = pygame.mixer.Sound('path_to_sound_file.wav')

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    # 이미지를 RGB로 변환
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    # 손을 감지하면 사운드 재생
    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)
            # 여기서 손의 위치에 따라 다른 사운드를 재생하도록 조건을 추가할 수 있습니다.
            sound.play()

    cv2.imshow('Hand Tracking with Sound', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
