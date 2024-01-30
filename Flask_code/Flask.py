from flask import Flask, render_template, request
import os
import cv2
import time

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
        receive_frame(frame_data)  # Call the function directly
        time.sleep(0.1)  # Adjust the sleep time if needed
    cap.release()


def receive_frame(frame_data):
    global frame_counter
    frame_counter += 1

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], f'frame_{frame_counter}.jpg')
    with open(file_path, 'wb') as file:
        file.write(frame_data)
    print('Frame received and saved successfully')


@app.route('/')
def index():
    path_live = RUN_FOLDER
    return render_template('index.html', path_live=path_live)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True,use_reloader=False)
