import cv2
import os
from app.config import Config
from werkzeug.utils import secure_filename
import threading

class RecordingThread(threading.Thread):
    def __init__(self, name, camera):
        threading.Thread.__init__(self)
        self.name = name
        self.isRunning = True

        self.cap = camera
        # fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            Config.UPLOAD_FOLDER,
            secure_filename('video.mp4')
        )
        self.out = cv2.VideoWriter(path, -1, 20.0, (640,480))

    def run(self):
        while self.isRunning:
            ret, frame = self.cap.read()
            frame = cv2.flip(frame, 1)
            if ret:
                self.out.write(frame)

        self.out.release()

    def stop(self):
        self.isRunning = False

    def __del__(self):
        self.out.release()

class VideoCamera(object):
    def __init__(self):
        # Open a camera
        self.cap = cv2.VideoCapture(0)
      
        # Initialize video recording environment
        self.is_record = False
        self.out = None

        # Thread for recording
        self.recordingThread = None
    
    def __del__(self):
        self.cap.release()
    
    def get_frame(self):
        ret, frame = self.cap.read()
        frame = cv2.flip(frame, 1)

        if ret:
            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()
        return None

    def start_record(self):
        self.is_record = True
        self.recordingThread = RecordingThread("Video Recording Thread", self.cap)
        self.recordingThread.start()

    def stop_record(self):
        self.is_record = False

        if self.recordingThread:
            self.recordingThread.stop()

            