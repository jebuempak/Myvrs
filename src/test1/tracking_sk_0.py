import cv2
import mediapipe as mp
import time
# MediaPipe Pose 모델 초기화
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# 웹캠 초기화
cap = cv2.VideoCapture(0)

while True:
	ret, frame = cap.read()
	if not ret:
		break

	# 프레임을 RGB로 변환
	rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

	# 포즈 추적
	results = pose.process(rgb_frame)

	# 스켈레톤 그리기
	if results.pose_landmarks:
		mp_drawing = mp.solutions.drawing_utils
		mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
		print( results.pose_landmarks )
		#print( mp_pose.POSE_CONNECTIONS )
	else:
		print("")

	# 화면에 출력
	cv2.imshow('Pose Estimation', frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	
	time.sleep(0.1)

# 리소스 해제
cap.release()
cv2.destroyAllWindows()
