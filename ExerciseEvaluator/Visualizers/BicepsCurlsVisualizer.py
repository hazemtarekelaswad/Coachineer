from Common.Imports import *
from Visualizers.Visualizer import Visualizer

class BicepsCurlsVisualizer(Visualizer):

    def visualize(self):
        frame_index = 0
        while True:
            in_progress, frame = self.video.read()

            # Check if it is finished
            if not in_progress:
                print('Video is finished')
                break
            
            rep = self.evaluation.loc[frame_index, 'rep']
            error_1 = self.evaluation.loc[frame_index, 'error_1']
            error_2 = self.evaluation.loc[frame_index, 'error_2']
            
            cv2.rectangle(
                img = frame, 
                pt1 = (0,0), 
                pt2 = (300,100), 
                color = (245,117,16), 
                thickness = -1
            )
            
            cv2.putText(
                img = frame,
                text = f'Rep: {rep + 1 if rep != -1 else "Incompleted"}',
                org = (15, 20),
                fontFace = cv2.FONT_HERSHEY_SIMPLEX,
                fontScale = 0.4,
                color = (0, 0, 0),
                thickness = 1,
                lineType = cv2.LINE_AA   
            )

            cv2.putText(
                img = frame,
                text = f'Upper arm: {"Too much rotation:(" if error_1 else "Correct :)"}',
                org = (15, 40),
                fontFace = cv2.FONT_HERSHEY_SIMPLEX,
                fontScale = 0.4,
                color = (0, 0, 0),
                thickness = 1,
                lineType = cv2.LINE_AA   
            )

            cv2.putText(
                img = frame,
                text = f'Forearm: {"Not full range of motion:(" if error_2 else "Correct :)"}',
                org = (15, 60),
                fontFace = cv2.FONT_HERSHEY_SIMPLEX,
                fontScale = 0.4,
                color = (0, 0, 0),
                thickness = 1,
                lineType = cv2.LINE_AA   
            )
            
            cv2.imshow('Video', frame)

            frame_index += 1

            if cv2.waitKey(25) == ord('q'):
                break
        cv2.destroyAllWindows()
        