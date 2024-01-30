from flask import Flask, request,render_template,Response
import os
import cv2
import requests
import time
from flask import send_file
import numpy as np
from io import BytesIO

app = Flask(__name__)

STATIC_FOLDER = 'Footage'
app.config['STATIC_FOLDER'] = STATIC_FOLDER

MAX_FRAMES = float('inf')  # No limit on the number of frames
frame_counter = 0  # Counter to keep track of frames received
def create_run_folder():
    timestamp = time.strftime("%Y%m%d_%H%M")
    run_folder = os.path.join(app.config['STATIC_FOLDER'], f'upload_{timestamp}')
    try:
        os.mkdir(run_folder)
    except FileExistsError:
        print(f"Folder '{run_folder}' already exists.")

    return run_folder


RUN_FOLDER = create_run_folder()
UPLOAD_FOLDER = RUN_FOLDER
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
        time.sleep(0.1)  # Adjust the sleep time if needed
    cap.release()
    #return 'Camera feed stopped'


@app.route('/receive_frame_route', methods=['POST'])
def receive_frame():
    global frame_counter
    frame_counter += 1

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], f'frame_{frame_counter}.jpg')
    with open(file_path, 'wb') as file:
        file.write(request.data)
    return 'Frame received and saved successfully', 200

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/latest_frame')
def latest_frame():
    global frame_counter
    frame_path = os.path.join(app.config['UPLOAD_FOLDER'], f'frame_{frame_counter}.jpg')
    return send_file(frame_path, mimetype='image/jpg')


if __name__ == '__main__':
    print("Hi how are you")
    app.run('0.0.0.0',port=5000, debug=True)


