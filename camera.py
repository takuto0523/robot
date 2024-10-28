import cv2

cap = cv2.VideoCapture(0)

# カメラがサポートしているFPSを取得
fps = cap.get(cv2.CAP_PROP_FPS)
print("カメラがサポートしているFPS:", fps)

cap.release()
