import cv2
import mediapipe as mp
import pyautogui
import mouse
import threading

# initialize
cam = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands.Hands(max_num_hands=1)
SCREEN_W, SCREEN_H = pyautogui.size()
pyautogui.FAILSAFE = False

def isPointsClose(two_points, axis):
    if axis == 'x':
        points_distance = int((two_points[0].x - two_points[1].x) * 100)
    else:
        points_distance = int((two_points[0].y - two_points[1].y) * 100)
    return (points_distance >= -3 and points_distance <= 3)

def click(button='left', count=None):
    if count != 1:
        pyautogui.click(button=button)
    else:
        pyautogui.click(button=button, clicks=count)
    pytautogui.sleep(1)

def moveCursor(move_cursor_point):
    sensitive = 1.5
    screen_w = SCREEN_W * sensitive
    screen_h = SCREEN_h * sensitive

    """
    since the screen size is multiplied with sensitive, that mean...
    to make the pointer reach the top right of screen display, 
    computer vision does not need to to reach top right of camera frame.
    so there is a unused spaces in top right of camera frame, since 0 axis is on top right.

    so the coordinates need to be reduced to center 
    """

    screen_w_offset = SCREEN_W / (sensitive * 2)
    screen_h_offset = SCREEN_H / (sensitive * 2)
    
    cursor_x = (move_cursor_point.x * screen_w) - screen_w_offset
    cursor_y = (move_cursor_point.y * screen_h) - screen_h_offset
    cursor_coordinates = [cursor_x, cursor_y]

    pyautogui.moveTo(cursor_x, cursor_y)

def drag(move_cursor_point, button="left"):
    sensitive = 1.5
    
    screen_w = SCREEN_W * sensitive
    screen_h = SCREEN_h * sensitive

    screen_w_offset = SCREEN_W / (sensitive * 2)
    screen_h_offset = SCREEN_H / (sensitive * 2)
    
    cursor_x = (move_cursor_point.x * screen_w) - screen_w_offset
    cursor_y = (move_cursor_point.y * screen_h) - screen_h_offset
    cursor_coordinates = [cursor_x, cursor_y]

    pyautogui.dragTo(cursor_x, cursor_y)

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

        # finger points
        tumb_tip = hand_landmarks[4]
        index_tip = hand_landmarks[8]
        middle_tip = hand_landmarks[12]
        ring_tip = hand_landmarks[16]
        pinky_tip = hand_landmarks[20]

        landmarks_to_draw = [
            index_tip, tumb_tip, middle_tip, ring_tip, pinky_tip
        ]        

        # finger index for command
        move_cursor_point = index_tip
        left_click_points = [tumb_tip, middle_tip]
        right_click_points = [tumb_tip, ring_tip]
        double_click_points = [tumb_tip, pinky_tip]
        drag_points = [
            [tumb_tip, middle_tip],
            [tumb_tip, ring_tip],
            [tumb_tip, pinky_tip],
        ]

        # move cursor
        threading.Thread(target=moveCursor, args=(move_cursor_point,)).start()
        # moveCursor(move_cursor_point)
        
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
        if (isPointsClose(drag_points[0], 'x') and isPointsClose(drag_points[1], 'x') and isPointsClose(drag_points[2], 'x')
            and isPointsClose(drag_points[0], 'y') and isPointsClose(drag_points[1], 'y') and isPointsClose(drag_points[2], 'y')):
            threading.Thread(target=drag, args=(move_cursor_point, "left",)).start()
        elif isPointsClose(left_click_points, axis='x') and isPointsClose(left_click_points, axis='y'):
            threading.Thread(target=click, args=('left',)).start()
            # click('left')
        elif isPointsClose(right_click_points, axis='x') and isPointsClose(right_click_points, axis='y'):
            threading.Thread(target=click, args=('right',)).start()
            # click('right')
        elif isPointsClose(double_click_points, axis='x') and isPointsClose(double_click_points, axis='y'):
            threading.Thread(target=click, args=('left',2,)).start()
            # click('left', 2)
        
    # create window
    cv2.imshow('Eye Controlled Mouse', frame)
    cv2.waitKey(1)
