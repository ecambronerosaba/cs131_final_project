from cvzone.HandTrackingModule import HandDetector
import cv2
import pyautogui
from time import sleep


def press_button(button_name, time_of_button_press):
    pyautogui.press(button_name)
    pyautogui.keyUp(button_name)


def left_gesture_to_key(finger_count):
    if finger_count == 5:
        return 'SPACE'
    elif finger_count == 0:
        return 'z'


def right_gesture_to_key(finger_count):
    if finger_count == 0:
        return 'z'
    if finger_count == 1:
        return 'd'
    elif finger_count == 2:
        return 'a'
    elif finger_count == 3:
        return 's'
    elif finger_count == 4:
        return 'w'
    elif finger_count == 5:
        return 'p'


button_name = "d"  # string
time_of_button_press = 1  # interger

press_button(button_name, time_of_button_press)

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)
save_right = None
save_left = None
while True:
    # Get image frame
    success, img = cap.read()
    # Find the hand and its landmarks
    hands, img = detector.findHands(img)  # with draw
    # hands = detector.findHands(img, draw=False)  # without draw

    if len(hands) == 2:
        # Hand 1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  # List of 21 Landmark points
        bbox1 = hand1["bbox"]  # Bounding box info x,y,w,h
        centerPoint1 = hand1['center']  # center of the hand cx,cy
        handType1 = hand1["type"]  # Handtype Left or Right

        # Hand 2
        hand2 = hands[1]
        lmList2 = hand2["lmList"]  # List of 21 Landmark points
        bbox2 = hand2["bbox"]  # Bounding box info x,y,w,h
        centerPoint2 = hand2['center']  # center of the hand cx,cy
        handType2 = hand2["type"]  # Hand Type "Left" or "Right"

        fingers2 = detector.fingersUp(hand2)
        fingers1 = detector.fingersUp(hand1)

        right_key = right_gesture_to_key(fingers1.count(
            1)) if handType1 == 'Right' else right_gesture_to_key(fingers2.count(1))

        left_key = left_gesture_to_key(fingers1.count(
            1)) if handType1 == 'Left' else left_gesture_to_key(fingers2.count(1))

        if right_key:
            if right_key != 'z':
                save_right = right_key
                pyautogui.keyDown(right_key)
            if save_right and right_key == 'z':
                pyautogui.keyUp(save_right)

        if left_key:
            if left_key != 'z':
                pyautogui.keyDown(left_key)
                save_left = left_key
            if save_left and left_key == 'z':
                pyautogui.keyUp(save_left)

    # Display
    cv2.imshow("Image", img)
    cv2.waitKey(1)
cap.release()
cv2.destroyAllWindows()
