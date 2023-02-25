from Common.Imports import *

class VideoReader:
    def __init__(self, video_path):
        self.video = cv2.VideoCapture(video_path)

        # Error handling
        if not self.video.isOpened():
            print(f'Error reading the video path {video_path}')
            self.video = None
    
    def __del__(self):
        self.video.release()
        print('Video is released')
        