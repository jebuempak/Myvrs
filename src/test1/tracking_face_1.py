import cv2
import dlib

# dlib의 얼굴 검출기 초기화
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")  # dlib의 얼굴 랜드마크 모델 파일 경로

# 웹캠 초기화
cap = cv2.VideoCapture(0)

while True:
	ret, frame = cap.read()
	if not ret:
		break

	# 그레이스케일로 변환
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# 얼굴 검출
	faces = detector(gray)

	for face in faces:
		# 얼굴 윤곽 포인트 추출
		landmarks = predictor(gray, face)

		# 얼굴 윤곽 그리기
		for i in range(68):  # 68개의 얼굴 랜드마크
			x, y = landmarks.part(i).x, landmarks.part(i).y
			cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)

	# 화면 분할 및 아바타 생성
	avatar = frame  # 여기에 원하는 아바타 이미지를 추가하세요

	# 화면에 출력
	cv2.imshow('Avatar', avatar)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# 리소스 해제
cap.release()
cv2.destroyAllWindows()
