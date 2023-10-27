from cvzone.FaceMeshModule import FaceMeshDetector
import cv2

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Initialize FaceMeshDetector object
detector = FaceMeshDetector(staticMode=False, maxFaces=2, minDetectionCon=0.5, minTrackCon=0.5)

def draw_teddy_face(img, face):
    # Draw a circle for the face
    x, y, w, h = cv2.boundingRect(face)
    center = (x + w // 2, y + h // 2)
    radius = min(w, h) // 2
    cv2.circle(img, center, radius, (80, 42, 42), -1)  # Brown color
    
    # Draw circles for the ears
    ear_radius = radius // 2
    cv2.circle(img, (center[0] - ear_radius - radius // 4, center[1] - ear_radius), ear_radius, (80, 42, 42), -1)
    cv2.circle(img, (center[0] + ear_radius + radius // 4, center[1] - ear_radius), ear_radius, (80, 42, 42), -1)
    
    # Draw circles for the eyes
    eye_radius = radius // 5
    eye_x_offset = radius // 2
    eye_y_offset = radius // 3
    cv2.circle(img, (center[0] - eye_x_offset, center[1] - eye_y_offset), eye_radius, (255, 255, 255), -1)
    cv2.circle(img, (center[0] + eye_x_offset, center[1] - eye_y_offset), eye_radius, (255, 255, 255), -1)

    # Draw a circle for the nose
    nose_radius = radius // 6
    cv2.circle(img, center, nose_radius, (0, 0, 0), -1)
    
    # Draw a line for the mouth
    mouth_y_offset = radius // 2
    cv2.line(img, (center[0] - eye_x_offset, center[1] + mouth_y_offset),
                  (center[0] + eye_x_offset, center[1] + mouth_y_offset), (0, 0, 0), 2)

# Start the loop to continually get frames from the webcam
while True:
    # Read the current frame from the webcam
    success, img = cap.read()

    # Find face mesh in the image
    img, faces = detector.findFaceMesh(img, draw=False)

    # Check if any faces are detected
    if faces:
        # Loop through each detected face
        for face in faces:
            draw_teddy_face(img, face)

    # Display the image in a window named 'Image'
    cv2.imshow("Image", img)

    # Wait for 1 millisecond to check for any user input, keeping the window open
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
