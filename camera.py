import cv2
import numpy as np

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        assert self.video.isOpened(), 'Cannot capture source'
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        # success, image = self.video.read()
        # # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # # so we must encode it into JPEG in order to correctly display the
        # # video stream.
        # # 画像をメモリ上で圧縮する（encode）
        # ret, jpeg = cv2.imencode('.jpg', image)
        # return jpeg.tobytes()
        try:   
            while True:
                r, f = self.video.read()
                if f is None:
                    print('--(!) No captured frame -- Break!')
                    break
                
                h, w = f.shape[:2]
                mask = np.zeros((h,w), dtype = np.uint8)
                bgdModel = np.zeros((1,65),np.float64)
                fgdModel = np.zeros((1,65),np.float64)
                rect=(1,1,w,h)
                cv2.grabCut(f, mask, rect, bgdModel, fgdModel, 10, cv2.GC_INIT_WITH_RECT)
                mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
                img2 = f*mask2[:,:,np.newaxis]
                #cv2.imshow("f", f)
                #cv2.imshow("img2", img2)
                # 画像をメモリ上で圧縮する（encode）
                ret, jpeg = cv2.imencode('.jpg', img2)
                return jpeg.tobytes()
                
                if cv2.waitKey(10) == 27:
                    break

        except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
            print("\nCamera Interrupt")

        # finally:
        #     self.video.release()
        #     cv2.destroyAllWindows()