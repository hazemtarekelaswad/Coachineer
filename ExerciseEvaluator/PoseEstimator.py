from Body import Body
from BodySequence import BodySequence

from Imports import *

class PoseEstimator:
    def __init__(self, video):
        self.video = video

    
    ################### Private methods ###################
    '''
    pose_obj: is the pose object obtained from mediapipe
    frame_number: 0-based frame number

    returns:
        Body: Body object with 33 Joints inside, only if the video is still in progress
        or None: once finished
    '''
    def _estimate_frame(self, pose_obj, frame_number) -> Body:
        in_progress, frame = self.video.read()

        # Check if it is finished
        if not in_progress:
            print('Video is finished')
            return None

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame.flags.writeable = False

        keypoints = pose_obj.process(frame)

        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        body = Body(frame_number)
        body.fill(keypoints.pose_landmarks.landmark)

        
        ################# Drawing utility #################
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing.draw_landmarks(
            frame, 
            keypoints.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
        )

        cv2.imshow('Video', frame)
        ###################################################

        return body


    ################### Public methods ###################
    '''
    returns:
        BodySequence: BodySequence object with all the bodies in each frame inside
    '''
    def estimate_sequence(self) -> BodySequence:
        with mp.solutions.pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            body_sequence = BodySequence()

            frame_number = 0
            body = self._estimate_frame(pose, frame_number)
            while body:
                body_sequence.append(body)
                frame_number += 1
                body = self._estimate_frame(pose, frame_number)
                if cv2.waitKey(25) == ord('q'):
                    break
            
            cv2.destroyAllWindows()
        
            return body_sequence