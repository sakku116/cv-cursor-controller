import cv2
import mediapipe as mp
import pyautogui
import mouse
import threading

# initialize
cam = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands.Hands(max_num_hands=1)
screen_w, screen_h = pyautogui.size()
pyautogui.FAILSAFE = False

def isPointsClose(two_points, axis):
    if axis == 'x':
        points_distance = int((two_points[0].x - two_points[1].x) * 100)
    else:
        points_distance = int((two_points[0].y - two_points[1].y) * 100)
    return (points_distance >= -3 and points_distance <= 3)

def click(button='left', count=None):
    if count != 1:
        mouse.click(button)
    else:
        mouse.click(button, clicks=count)

def moveCursor(move_cursor_point):
    sensitive = 1.5
    cursor_x = ((move_cursor_point.x) * (screen_w * sensitive)) - (screen_w / 3)
    cursor_y = ((move_cursor_point.y) * (screen_h * sensitive)) - (screen_h / 3)
    cursor_coordinates = [cursor_x, cursor_y]
    mouse.move(cursor_x, cursor_y)

while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_process = mp_hands.process(frame)
    multi_hand_landmarks = mp_process.multi_hand_landmarks

    # get size of the frame
    frame_h, frame_w, _ = frame.shape

    if multi_hand_landmarks:
        hand_landmarks = multi_hand_landmarks[0].landmark
        landmarks_to_draw = [
            hand_landmarks[5], hand_landmarks[4], 
            hand_landmarks[12], hand_landmarks[16],
            hand_landmarks[20]
        ] # base index, thumb tip, middle tip, ring tip, pinky tip

        # finger points
        move_cursor_point = hand_landmarks[5] # base index finger
        left_click_points = [hand_landmarks[4], hand_landmarks[12]] # thumb tip, middle tip
        right_click_points = [hand_landmarks[4], hand_landmarks[16]] # thumb tip, ring tip
        double_click_points = [hand_landmarks[4], hand_landmarks[20]] # thumb tip, pinky tip

        # move cursor
        threading.Thread(target=moveCursor, args=(move_cursor_point,)).start()
        
        # draw landmarks
        for landmark_id, landmark in enumerate(landmarks_to_draw):
            # draw on particular landmark
            draw_coordinates = (
                int(landmark.x * frame_w), # x
                int(landmark.y * frame_h) # y
            )

            if landmark_id == 0: # pointer
                rgb = (0, 0, 255)
                size = 7
                threading.Thread(target=cv2.circle, args=(frame, draw_coordinates, size, rgb, cv2.FILLED,)).start()

            else:
                rgb = (0, 255, 255)
                size = 10
                threading.Thread(target=cv2.circle, args=(frame, draw_coordinates, size, rgb,)).start()

        # click events
        if isPointsClose(left_click_points, axis='x') and isPointsClose(left_click_points, axis='y'):
            threading.Thread(target=click, args=('left',)).start()
        if isPointsClose(right_click_points, axis='x') and isPointsClose(right_click_points, axis='y'):
            threading.Thread(target=click, args=('right',)).start()
        if isPointsClose(double_click_points, axis='x') and isPointsClose(double_click_points, axis='y'):
            threading.Thread(target=click, args=('left',2,)).start()

        
    # create window
    cv2.imshow('Eye Controlled Mouse', frame)
    cv2.waitKey(1)
