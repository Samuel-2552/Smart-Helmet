from flask import Flask, request
import os
import cv2
import requests
import time

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Input route for camera feed
@app.route('/camera_feed')
def camera_feed():
    cap = cv2.VideoCapture(0)  # Use default camera (index 0)
    while True:
        success, image = cap.read()
        if not success:
            break
        _, img_encoded = cv2.imencode('.jpg', image)
        frame_data = img_encoded.tobytes()
        url = 'http://127.0.0.1:5001/receive_frame_route'  # Route to 5001 for saving frames
        requests.post(url, data=frame_data)
    cap.release()
    return 'Camera feed stopped'


MAX_FRAMES = 500  # Number of frames to store, adjust as needed
frame_counter = 0  # Counter to keep track of frames received


def overwrite_frames():
    for i in range(1, MAX_FRAMES + 1):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f'frame_{i}.jpg')
        if os.path.exists(file_path):
            os.remove(file_path)

        new_frame_data = request.data  # Get new frame data here
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], f'frame_{i}.jpg')
        with open(file_path, 'wb') as file:
            file.write(new_frame_data)


@app.route('/receive_frame_route', methods=['POST'])
def receive_frame():
    global frame_counter
    frame_counter += 1

    file_count = frame_counter % MAX_FRAMES or MAX_FRAMES
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], f'frame_{file_count}.jpg')
    with open(file_path, 'wb') as file:
        file.write(request.data)

    if frame_counter >= MAX_FRAMES:
        overwrite_frames()  # Overwrite frames from 1 to 10

    return 'Frame received and saved successfully', 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)
