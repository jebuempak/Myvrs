import cv2
import mediapipe as mp
import time

# MediaPipe Hands 모델 초기화
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# OpenCV 비디오 캡처 초기화
cap = cv2.VideoCapture(0)
#cv2.resizeWindow("Video", 500, 500)

while cap.isOpened():
	ret, frame = cap.read()
	if not ret:
		continue
	print( "1")

	# BGR 이미지를 RGB 이미지로 변환
	rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

	# MediaPipe Hands를 사용하여 손 검출
	results = hands.process(rgb_frame)


	if results.multi_hand_landmarks:
		for landmarks in results.multi_hand_landmarks:
			for lm in landmarks.landmark:
				h, w, c = frame.shape
				cx, cy = int(lm.x * w), int(lm.y * h)
				print( cx, cy)
				cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
				

	cv2.imshow("Hand Tracking", frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
