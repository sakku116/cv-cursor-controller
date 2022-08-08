import cv2
import mediapipe as mp
import pyautogui

# initialize
cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()

while True:
    # read every frame from camera
    _, frame = cam.read()
    # flip the frame horizontally
    frame = cv2.flip(frame, 1)
    # convert color to make the face_mesh easier to detect face
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # process the frame using mediapipe
    output = face_mesh.process(rgb_frame)
    # get the point of multiple face landmarks (return list of dictionary for each face)
    landmark_points = output.multi_face_landmarks

    # get size of the frame
    frame_h, frame_w, _ = frame.shape

    if landmark_points:
        ''' extracting the points '''
        # get only one face
        landmarks = landmark_points[0].landmark # return list from the dict containing many points, and each point contain x and y
        eye_landmarks = landmarks[474:478]

        # draw eye points
        for id, landmark in enumerate(eye_landmarks):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            coordinates = (x,y)
            size = 3
            rgb = (0, 255, 0)
            cv2.circle(frame, coordinates, size, rgb)

            # control cursor
            if id == 1: # only get one point from landmarks to take the control
                cursor_x = screen_w / frame_w * x
                cursor_y = screen_h / frame_h * y
                pyautogui.moveTo(cursor_x, cursor_y)

        left_eye_landmarks = [landmarks[145], landmarks[159]]
        # draw face in the frame
        for landmark in left_eye_landmarks:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            coordinates = (x,y)
            size = 4
            rgb = (0, 255, 0)
            cv2.circle(frame, coordinates, size, rgb)

        # detect blink from left eye to control click
        if (left_eye_landmarks[0].y - left_eye_landmarks[1].y) < 0.004: # they are so close
            pyautogui.click()
            # prevent clicking continously
            pyautogui.sleep(1)

    # create window
    cv2.imshow('Eye Controlled Mouse', frame)
    cv2.waitKey(1)
