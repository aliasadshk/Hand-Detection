import cv2
import mediapipe as mp
import pyautogui

# Function to detect and draw hand gestures
def detect_and_draw_hand_gestures():
    cap = cv2.VideoCapture(0)

    # Create a Mediapipe Hands object
    mp_hands = mp.solutions.hands.Hands()
    # Define drawing utility
    mp_drawing = mp.solutions.drawing_utils

    frame_skip = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the image to RGB and process it with Mediapipe Hands
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = mp_hands.process(image)

        # Check if hands are detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks on the image using cv2.circle()
                for idx, landmark in enumerate(hand_landmarks.landmark):
                    x = int(landmark.x * image.shape[1])
                    y = int(landmark.y * image.shape[0])
                    cv2.circle(image, (x, y), 5, (0, 0, 255), -1)

                # Process hand landmarks to detect gestures
                # Example: Label hand as open or closed based on thumb and finger positions
                thumb_tip = hand_landmarks.landmark[4]  # Thumb tip landmark index
                index_finger_tip = hand_landmarks.landmark[8]  # Index finger tip landmark index
                distance = cv2.norm(
                    (thumb_tip.x, thumb_tip.y), (index_finger_tip.x, index_finger_tip.y)
                )

                hand_label = "Open" if distance > 0.1 else "Closed"

                # Determine hand face direction (right or left)
                wrist = hand_landmarks.landmark[0]  # Wrist landmark index
                thumb = hand_landmarks.landmark[4]  # Thumb tip landmark index

                if thumb.x < wrist.x + 0.15 and thumb.x > wrist.x - 0.14 and thumb.y > wrist.y:
                    hand_direction = "Down"
                elif thumb.x < wrist.x + 0.15 and thumb.x > wrist.x - 0.14 and thumb.y < wrist.y:
                    hand_direction = "Up"
                elif thumb.x < wrist.x:
                    hand_direction = "Left"
                else:
                    hand_direction = "Right"

                # Count the number of fingers raised
                finger_count = 0
                finger_landmark_ids = [4, 8, 12, 16, 20]  # Landmark IDs of finger tips
                for landmark_id in finger_landmark_ids:
                    landmark = hand_landmarks.landmark[landmark_id]
                    if landmark.y < hand_landmarks.landmark[landmark_id - 2].y:
                        finger_count += 1

                if frame_skip <= 0:
                    if hand_label == "Open" :
                        # pyautogui.press('play')
                        # frame_skip = frame_skip + 1
                        if hand_direction == 'Up':
                            pyautogui.press('up')
                            print('Up')
                        if hand_direction == 'Down':
                            pyautogui.press('down')
                            print('Down')
                        if hand_direction == 'Right':
                            pyautogui.press('left')
                            print('right')
                        if hand_direction == 'Left':
                            pyautogui.press('right')
                            print('left')
                    # elif hand_label == "Closed":
                        # pyautogui.press('Pause')
                        # print('pause')

                    # Perform actions based on the finger count
                    # if finger_count == 1:
                    #     pyautogui.press('1')
                    #     print('1 finger raised')
                    # elif finger_count == 2:   
                    #     pyautogui.press('2')
                    #     print('2 fingers raised')
                    if finger_count == 3:
                        pyautogui.press('space')
                        print('3 fingers raised')
                    # elif finger_count == 4:
                    #     pyautogui.press('tab')
                    #     print('4 fingers raised')
                    # elif finger_count == 5:
                    #     pyautogui.keyDown('alt')
                    #     pyautogui.press('tab')
                    #     pyautogui.keyUp('alt')
                    #     print('5 fingers raised')
                    print(finger_count)
                else:
                    frame_skip = 0

                # Display hand label, direction, and finger count on the image
                cv2.putText(
                    image,
                    f"Hand: {hand_label}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2,
                    cv2.LINE_AA,
                )

                cv2.putText(
                    image,
                    f"Direction: {hand_direction}",
                    (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2,
                    cv2.LINE_AA,
                )

                cv2.putText(
                    image,
                    f"Finger Count: {finger_count}",
                    (10, 90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2,
                    cv2.LINE_AA,
                )

        # Display the resulting frame
        cv2.imshow("Hand Gestures", cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

        # Exit when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

detect_and_draw_hand_gestures()