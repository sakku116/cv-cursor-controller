import cv2
import mediapipe as mp
import pyautogui
import mouse

# initialize
cam = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands.Hands(max_num_hands=1)
screen_w, screen_h = pyautogui.size()

def isPointsClose(two_points, axis):
    if axis == 'x':
        points_distance = int((two_points[0].x - two_points[1].x) * 100)
    else:
        points_distance = int((two_points[0].y - two_points[1].y) * 100)
    return (points_distance >= -3 and points_distance <= 3)

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
            if landmark_id == 5 or landmark_id == 4 or landmark_id == 12 or landmark_id == 16:
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                draw_coordinates = (x,y)

                if landmark_id == 5:
                    size = 15
                    rgb = (255, 255, 0)
                else:
                    size = 10
                    rgb = (0, 255, 255)

                cv2.circle(frame, draw_coordinates, size, rgb)

            # control cursor
            if landmark_id == 5: # only get one point from landmarks to take the control
                sensitive = 1.5
                cursor_x = ((landmark.x) * (screen_w * sensitive)) - (screen_w / 3)
                cursor_y = ((landmark.y) * (screen_h * sensitive)) - (screen_h / 3)
                cursor_coordinates = [cursor_x, cursor_y]
                mouse.move(cursor_x, cursor_y)

        left_click_points = [hand_landmarks[4], hand_landmarks[12]]
        right_click_points = [hand_landmarks[4], hand_landmarks[16]]
        if isPointsClose(left_click_points, axis='x') and isPointsClose(left_click_points, axis='y'): # they are so close
            mouse.click('left')
        if isPointsClose(right_click_points, axis='x') and isPointsClose(right_click_points, axis='y'): # they are so close
            mouse.click('right')

    # create window
    cv2.imshow('Eye Controlled Mouse', frame)
    cv2.waitKey(1)
