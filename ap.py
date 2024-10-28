import cv2
import pupil_apriltags

# カメラの設定
cap = cv2.VideoCapture(0)  # 0はデフォルトカメラ

# AprilTag検出器の初期化
at_detector = pupil_apriltags.Detector()

while True:
    # カメラからフレームを取得
    ret, frame = cap.read()
    if not ret:
        break

    # カラー画像をグレースケールに変換
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # エイプリルタグを検出
    tags = at_detector.detect(gray_frame)

    # 特定のタグ ID のみを描画
    for tag in tags:
        if tag.tag_id == 1:  # ID が 1 の場合のみ処理
            # タグの境界ボックスを描画
            cv2.polylines(frame, [tag.corners.astype(int)], isClosed=True, color=(0, 255, 0), thickness=2)
            # タグのIDを描画
            cv2.putText(frame, str(tag.tag_id), (int(tag.center[0]), int(tag.center[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # 結果を表示
    cv2.imshow('AprilTag Detection', frame)

    # 'q'キーで終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
