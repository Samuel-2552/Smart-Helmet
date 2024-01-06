from flask import Flask, request
import os
import cv2
import requests

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return "<h1>Home page</h1>"

# input route
@app.route('/inp')
def inp_frame():

    video_path = 'rec.mp4' # Video file
    cap = cv2.VideoCapture(video_path)
    success, image = cap.read()

    while success:
        _, img_encoded = cv2.imencode('.jpg', image)
        frame_data = img_encoded.tobytes()
        url = 'http://127.0.0.1:5000/receive_frame_route'
        requests.post(url, data=frame_data)
        success, image = cap.read()

#Output route
@app.route('/receive_frame_route', methods=['POST'])
def receive_frame():
    frame_data = request.data
    file_count = len(os.listdir(UPLOAD_FOLDER)) + 1
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], f'frame_{file_count}.jpg')
    with open(file_path, 'wb') as file:
        file.write(frame_data)
    return 'Frame received and saved successfully', 200

if __name__ == '__main__':
    app.run(debug=True)

