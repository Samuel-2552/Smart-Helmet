from flask import Flask, request,render_template,Response
import os
import cv2
import requests
import time
from flask import send_file
import numpy as np


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



if __name__ == '__main__':
    print("Hi how are you")
    app.run('0.0.0.0',port=5000, debug=True)


