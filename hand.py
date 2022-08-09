import cv2
import mediapipe as mp
import pyautogui
import mouse
import threading

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

def moveCursor(move_cursor_point, left_click_points, right_click_points):
    sensitive = 1.5
    cursor_x = ((move_cursor_point.x) * (screen_w * sensitive)) - (screen_w / 3)
    cursor_y = ((move_cursor_point.y) * (screen_h * sensitive)) - (screen_h / 3)
    cursor_coordinates = [cursor_x, cursor_y]
    mouse.move(cursor_x, cursor_y)

    if isPointsClose(left_click_points, axis='x') and isPointsClose(left_click_points, axis='y'): # they are so close
        pyautogui.click(button='left')
    if isPointsClose(right_click_points, axis='x') and isPointsClose(right_click_points, axis='y'): # they are so close
        pyautogui.click(button='right')

    pyautogui.sleep(.5)

def drawLandmarks(landmarks_to_draw):
    for landmark_id, landmark in enumerate(landmarks_to_draw):
        # draw on particular landmark
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

while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    #rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_process = mp_hands.process(frame)
    multi_hand_landmarks = mp_process.multi_hand_landmarks

    # get size of the frame
    frame_h, frame_w, _ = frame.shape

    if multi_hand_landmarks:
        hand_landmarks = multi_hand_landmarks[0].landmark
        landmarks_to_draw = [hand_landmarks[5], hand_landmarks[4], hand_landmarks[12], hand_landmarks[16]]

        cursor_coordinates = []
        move_cursor_point = hand_landmarks[5]
        left_click_points = [hand_landmarks[4], hand_landmarks[12]]
        right_click_points = [hand_landmarks[4], hand_landmarks[16]]

        # draw eye points
        draw_landmarks = threading.Thread(target=drawLandmarks, args=(landmarks_to_draw,))
        draw_landmarks.start()

        # control cursor
        control_cursor = threading.Thread(target=moveCursor, args=(move_cursor_point, left_click_points, right_click_points,))
        control_cursor.start()
        

    # create window
    cv2.imshow('Eye Controlled Mouse', frame)
    cv2.waitKey(1)
