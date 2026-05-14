from flask import Flask, render_template, Response, request
from flask_socketio import SocketIO
import cv2
import datetime
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)

# Camera storage
cameras = {
    0: 0  # Local webcam
}

def find_camera(id):
    try:
        return cameras[int(id)]
    except:
        return None

def gen_frames(camera_id):

    cam = find_camera(camera_id)

    if cam is None:
        raise Exception("Camera not found.")

    cap = cv2.VideoCapture(cam)

    while True:

        success, frame = cap.read()

        if not success:
            break

        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' +
                frame +
                b'\r\n'
            )

# ROUTES

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed/<string:id>/')
def video_feed(id):

    return Response(
        gen_frames(id),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

# REAL-TIME LOG GENERATOR

def generate_logs():

    sample_logs = [
        "Motion detected at Camera 1",
        "Unauthorized access attempt",
        "Camera connection stable",
        "Person detected in restricted area",
        "Face recognition triggered",
        "Low light detected",
        "System scan completed",
        "Object movement detected"
    ]

    while True:

        log = {
            "message": sample_logs[int(time.time()) % len(sample_logs)],
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        socketio.emit('new_log', log)

        time.sleep(3)

# START BACKGROUND THREAD

threading.Thread(target=generate_logs, daemon=True).start()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
