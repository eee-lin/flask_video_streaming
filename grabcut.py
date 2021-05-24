import cv2
import numpy as np

v = cv2.VideoCapture(0)

assert v.isOpened(), 'Cannot capture source'

try:   
    while True:
        r, f = v.read()
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
        cv2.imshow("f", f)
        cv2.imshow("img2", img2)
        
        if cv2.waitKey(10) == 27:
            break

except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    print("\nCamera Interrupt")

finally:
    v.release()
    cv2.destroyAllWindows()
