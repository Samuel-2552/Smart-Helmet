import cv2
import requests

url = 'http://127.0.0.1:5000/receive_frame_route'

cap = cv2.VideoCapture(0)

while True:
    success, image = cap.read()
    if not success:
        break
    _, img_encoded = cv2.imencode('.jpg', image)
    frame_data = img_encoded.tobytes()
    requests.post(url, data=frame_data)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('0'):
        break

cap.release()
cv2.destroyAllWindows()
