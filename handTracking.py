import sys
import cv2
import mediapipe as mp
from pythonosc import udp_client
import time
import config

# MediaPipe Pose 모델 초기화
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()


def send(incheck, right, left):
	try:
		# incheck 1: 사람들어옴, 0: 사람 나감
		client = udp_client.SimpleUDPClient(config.osc_server_ip, config.osc_server_port)
		client.send_message( "/human", incheck)
		if left < 0.0:
			left = 0.0
		
		if right < 0.0:
			right = 0.0
			
		client.send_message( "/left",  (round( left, 2)) )
		client.send_message( "/right", (round( right, 2)) )
		#client.send_message( '사람들어옴: /enter,  사람나감 /exit,  왼손: /left,  오른손: /right )
	except:
		pass


def main():
	mp_hands = mp.solutions.hands
	hands = mp_hands.Hands()
	mp_drawing = mp.solutions.drawing_utils

	cap = cv2.VideoCapture(0)
	
	human_incheck = 0
	left_float = 0.00
	right_float= 0.00

	while cap.isOpened():
		ret, frame = cap.read()

		if ret == True:
			human_incheck = 1
	
			# 손 추적
			rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			
			# 포즈 추적
			results = pose.process(rgb_image)
			# 스켈레톤 그리기
			if results.pose_landmarks:
				mp_drawing = mp.solutions.drawing_utils
				mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
				#print( results.pose_landmarks )
			else:
				human_incheck = 0
			
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
			send( human_incheck, send_hand_coordinates['left'], send_hand_coordinates['right'] )
			print( round( send_hand_coordinates['left'], 2), "|", round( send_hand_coordinates['right'], 2)  )
			time.sleep(0.05)
		
		cv2.imshow('Hand Tracking', frame)

		if cv2.waitKey(10) & 0xFF == ord('q'):
			break

	cap.release()
	cv2.destroyAllWindows()

if __name__ == "__main__":
    sys.exit(main())