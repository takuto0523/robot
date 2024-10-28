import cv2
import numpy as np

def get_wall_color():
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    
    print("Adjust the camera to focus on the wall and press 'c' to capture the wall color.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Wall Color Calibration", frame)
        if cv2.waitKey(1) & 0xFF == ord('c'):
            # Get the color from the center of the frame
            wall_color_bgr = frame[240, 320]
            break

    cap.release()
    cv2.destroyAllWindows()

    # Convert BGR color to HSV color
    wall_color_hsv = cv2.cvtColor(np.uint8([[wall_color_bgr]]), cv2.COLOR_BGR2HSV)[0][0]
    
    return wall_color_hsv

if __name__ == "__main__":
    wall_color_hsv = get_wall_color()
    print(f"Wall color in HSV: {wall_color_hsv}")
