import cv2

def capture_image():
    # カメラをキャプチャするためのVideoCaptureオブジェクトを作成
    cap = cv2.VideoCapture(0)

    # カメラからフレームを1つ取得
    ret, frame = cap.read()

    # フレームが正しく取得された場合
    if ret:
        # 画像を保存
        cv2.imwrite('captured_image.jpg', frame)
        print("Image captured successfully!")
    else:
        print("Failed to capture image!")

    # カメラを解放
    cap.release()

if __name__ == "__main__":
    capture_image()
