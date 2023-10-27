import sys
import cv2
import mediapipe as mp
from pythonosc import udp_client
import time
import config
import math

# MediaPipe Pose 모델 초기화
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

def send(incheck, right, left):
    try:
        client = udp_client.SimpleUDPClient(config.osc_server_ip, config.osc_server_port)
        client.send_message("/human", incheck)
        if left < 0.0:
            left = 0.0

        if right < 0.0:
            right = 0.0

        client.send_message("/left", round(left, 2))
        client.send_message("/right", round(right, 2))
    except:
        pass

def main():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    mp_drawing = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0)

    human_incheck = 0

    while cap.isOpened():
        ret, frame = cap.read()

        if ret == True:
            human_incheck = 1

            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            results = pose.process(rgb_image)
            if results.pose_landmarks:
                mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            else:
                human_incheck = 0

            results = hands.process(rgb_image)

            if results.multi_hand_landmarks:
                for landmarks in results.multi_hand_landmarks:
                    cx = int(sum([lmk.x for lmk in landmarks.landmark]) / len(landmarks.landmark) * frame.shape[1])
                    cy = int(sum([lmk.y for lmk in landmarks.landmark]) / len(landmarks.landmark) * frame.shape[0])

                    if cx <= frame.shape[1] / 2:
                        hand_type = 'left'
                    else:
                        hand_type = 'right'

                    normalized_x = cx / frame.shape[1]
                    normalized_y = cy / frame.shape[0]
                    cv2.putText(frame, f"{hand_type} (x: {normalized_x:.2f}, y: {normalized_y:.2f})", (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                    # 손목의 Y축 각도 계산
                    wrist = landmarks.landmark[0]  # wrist
                    mcp_joint = landmarks.landmark[9]  # MCP joint of middle finger

                    dx = mcp_joint.x - wrist.x
                    dy = mcp_joint.y - wrist.y

                    angle_rad = math.atan2(dy, dx)
                    angle_deg = math.degrees(angle_rad)

                    print(f"{hand_type} wrist Y-axis angle: {angle_deg:.2f} degrees")

                    mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)
                    
            send(human_incheck, normalized_x, normalized_y)
            time.sleep(0.05)

        cv2.imshow('Hand and Pose Tracking', frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    sys.exit(main())
