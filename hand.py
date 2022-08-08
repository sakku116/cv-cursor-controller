import cv2
import mediapipe as mp
import pyautogui
import mouse

# initialize
cam = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands.Hands(max_num_hands=1)
screen_w, screen_h = pyautogui.size()
print(screen_w)

while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_process = mp_hands.process(rgb_frame)
    multi_hand_landmarks = mp_process.multi_hand_landmarks

    # get size of the frame
    frame_h, frame_w, _ = frame.shape

    if multi_hand_landmarks:
        hand_landmarks = multi_hand_landmarks[0].landmark

        cursor_coordinates = []

        # draw eye points
        for landmark_id, landmark in enumerate(hand_landmarks):
            # draw on particular landmark
            if landmark_id == 5 or landmark_id == 4 or landmark_id == 12:
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                draw_coordinates = (x,y)

                if landmark_id == 5:
                    size = 15
                    rgb = (0, 255, 255)
                else:
                    size = 7
                    rgb = (0, 0, 255)

                cv2.circle(frame, draw_coordinates, size, rgb)

            # control cursor
            if landmark_id == 5: # only get one point from landmarks to take the control
                sensitive = 1.5
                cursor_x = ((landmark.x) * (screen_w * sensitive)) - (screen_w / 3)
                cursor_y = ((landmark.y) * (screen_h * sensitive)) - (screen_h / 3)
                cursor_coordinates = [cursor_x, cursor_y]
                mouse.move(cursor_x, cursor_y)

        index_finger_points = [hand_landmarks[12], hand_landmarks[4]]

        finger_points_distance_y = int((index_finger_points[0].y - index_finger_points[1].y) * 100)
        finger_points_distance_x = int((index_finger_points[0].x - index_finger_points[1].x) * 100)
        is_fingerPointsDistanceY_close = finger_points_distance_y >= -4 and finger_points_distance_y <= 4
        is_fingerPointsDistanceX_close = finger_points_distance_x >= -4 and finger_points_distance_x <= 4
        
        if is_fingerPointsDistanceY_close and is_fingerPointsDistanceX_close: # they are so close
            mouse.click('left')

    # create window
    cv2.imshow('Eye Controlled Mouse', frame)
    cv2.waitKey(1)
