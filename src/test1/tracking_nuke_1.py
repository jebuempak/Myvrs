import cv2
import nuke

# 웹캠 초기화
cap = cv2.VideoCapture(0)

while True:
    # 웹캠에서 프레임 캡처
    ret, frame = cap.read()
    if not ret:
        break
    
    # 프레임을 임시 이미지로 저장
    temp_path = "temp_frame.png"
    cv2.imwrite(temp_path, frame)

    # Nuke에서 이미지 읽기 및 처리
    read_node = nuke.nodes.Read(file=temp_path)
    blur_node = nuke.nodes.Blur(size=10)
    blur_node.setInput(0, read_node)
    nuke.execute(blur_node, 1, 1)  # Single frame execution

    # 처리된 이미지 로드 및 표시
    processed_frame = cv2.imread(temp_path)
    cv2.imshow('Processed Frame', processed_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
