import sys
import cv2
import mediapipe as mp
from pythonosc import udp_client
import time
import config
from sys import stdout

# MediaPipe Pose 모델 초기화
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

def send(incheck, left_wrist_y, right_wrist_y):
    try:
        client = udp_client.SimpleUDPClient(config.osc_server_ip, config.osc_server_port)
        client.send_message("/human", incheck)
        left_wrist_y = max(0.0, min(1.0, left_wrist_y))
        right_wrist_y = max(0.0, min(1.0, right_wrist_y))

        client.send_message("/left", left_wrist_y)
        client.send_message("/right", right_wrist_y)
    except:
        pass

def print_to_bottom(message):
    stdout.write("\033[K")  # 현재 라인 지우기
    stdout.write("\r" + message)  # 커서를 행의 시작으로 이동 후 메시지 출력
    stdout.flush()

def main():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    
    cap = cv2.VideoCapture(0)

    human_incheck = 0

    while cap.isOpened():
        ret, frame = cap.read()

        if ret == True:
            human_incheck = 1
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            results = pose.process(rgb_image)
            if results.pose_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            else:
                human_incheck = 0

            results = hands.process(rgb_image)
            
            left_wrist_y = 0.0
            right_wrist_y = 0.0

            if results.multi_hand_landmarks:
                for landmarks in results.multi_hand_landmarks:
                    wrist = landmarks.landmark[0]
                    if landmarks.landmark[mp_hands.HandLandmark.WRIST].x < 0.5:
                        left_wrist_y = 1 - wrist.y  # 값의 변화를 반전
                    else:
                        right_wrist_y = 1 - wrist.y  # 값의 변화를 반전

                    mp.solutions.drawing_utils.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

                message = f"Left wrist position: y={right_wrist_y:.2f}, Right wrist position: y={left_wrist_y:.2f}"
                print_to_bottom(message)
                    
            send(human_incheck, right_wrist_y, left_wrist_y)
            #time.sleep(0.05)

        cv2.imshow('Hand and Pose Tracking', frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    sys.exit(main())
