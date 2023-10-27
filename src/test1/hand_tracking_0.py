import cv2
import mediapipe as mp
from pythonosc import udp_client


def send(incheck, left, right):
	# incheck 1: 사람들어옴, 0: 사람 나감
	client = udp_client.SimpleUDPClient("127.0.0.1", 8000)
	client.send_message( "/enter", incheck)
	client.send_message("/exit", incheck ) 
	client.send_message( "/left", round(left, 2) )
	client.send_message("/right", round( right, 2) )
	#client.send_message( '사람들어옴: /enter,  사람나감 /exit,  왼손: /left,  오른손: /right )


mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

left_float = 0.00
right_float= 0.00

while cap.isOpened():
	ret, frame = cap.read()

	if not ret:
		continue

	# 손 추적
	rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	results = hands.process(rgb_image)

	hand_coordinates = {}

	send_hand_coordinates = {}
	send_hand_coordinates['left'] = 0.00
	send_hand_coordinates['right']= 0.00

	# 손의 중심점 찾기 및 x, y 좌표 출력
	if results.multi_hand_landmarks:
		for landmarks in results.multi_hand_landmarks:
			# 손 중심점 계산
			cx = int(sum([lmk.x for lmk in landmarks.landmark]) / len(landmarks.landmark) * frame.shape[1])
			cy = int(sum([lmk.y for lmk in landmarks.landmark]) / len(landmarks.landmark) * frame.shape[0])

			if cx <= frame.shape[1] / 2:  # 화면의 왼쪽 절반을 기준으로 왼손/오른손 분류
				hand_type = 'left'
			else:
				hand_type = 'right'

			normalized_x = cx / frame.shape[1]
			normalized_y = cy / frame.shape[0]
			hand_coordinates[hand_type] = ( round( normalized_x, 2), round( normalized_y, 2) )
			send_hand_coordinates[hand_type] = normalized_y
			

			cv2.putText(frame, f"{hand_type} (x: {normalized_x:.2f}, y: {normalized_y:.2f})", (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

			# 손 랜드마크 그리기
			mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)
	send( 1, send_hand_coordinates['left'], send_hand_coordinates['right'] )
	print(hand_coordinates)

	cv2.imshow('Hand Tracking', frame)

	if cv2.waitKey(10) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
