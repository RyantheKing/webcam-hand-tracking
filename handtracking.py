import cv2
import builtins
import numpy as np

#1) make sure your hands are out of frame.  Do not move your head out of frame and then put it back in, either always have it out, or always have it in.
#2) press x
#3) move hands into respective boxes

def findHandPos_standalone(x_size=0.5, threshold=60):
    """runs the hand tracking program given a vertical division and threshold"""
    y_size = 1
    cap = cv2.VideoCapture(0)

    bgModel = -1

    while True:
        # Capture frame-by-frame

        _, frame = cap.read()
        frame = cv2.bilateralFilter(frame, 5, 50, 100)
        frame=cv2.flip(frame,1) #mirror webcam
        #draw rectange frame for right hand
        cv2.rectangle(frame, (int(x_size * frame.shape[1]), 0),
                    (frame.shape[1], int(y_size * frame.shape[0])), (255, 0, 0), 2) #<-- dis thing makes the fancy rectangle to put thou hand in.
        #draw rectange frame for left hand
        cv2.rectangle(frame, (int((x_size-0.003) * frame.shape[1]), 0),
                    (0, int(y_size * frame.shape[0])), (0, 255, 0), 2) #<-- dis thing makes the fancy rectangle to put thou hand in.

        if cv2.waitKey(1) == ord('x'):
            bgModel = cv2.createBackgroundSubtractorMOG2(0, 50)

        #  big boi calculations
        if bgModel != -1:
            fgmask = bgModel.apply(frame,learningRate=0)
            kernel = np.ones((3, 3), np.uint8)
            fgmask = cv2.erode(fgmask, kernel, iterations=1)
            img = cv2.bitwise_and(frame, frame, mask=fgmask)
            #layout rectangular boundaries for each hand
            img1 = img[0:int(y_size * frame.shape[0]),
                        int(x_size * frame.shape[1]):frame.shape[1]]
            img2 = img[0:int(y_size * frame.shape[0]),
                        0:int(x_size * frame.shape[1])]
            
            gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
            gray3 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blur1 = cv2.GaussianBlur(gray1, (41, 41), 0) #<--blur boi 1
            blur2 = cv2.GaussianBlur(gray2, (41, 41), 0) #<--blur boi 2
            blur3 = cv2.GaussianBlur(gray3, (41, 41), 0) #<--blur boi 3 (combined 1 and 2)
            _, thresh1 = cv2.threshold(blur1, threshold, 255, cv2.THRESH_BINARY)
            _, thresh2 = cv2.threshold(blur2, threshold, 255, cv2.THRESH_BINARY)
            _, thresh3 = cv2.threshold(blur3, threshold, 255, cv2.THRESH_BINARY)

            # once B&W image is created, find Countours
            contours1, _ = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours2, _ = cv2.findContours(thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            length1 = len(contours1)
            length2 = len(contours2)
            maxArea = -1
            if length1 > 0:
                for i in range(length1): #find contour area
                    temp = contours1[i]
                    area = cv2.contourArea(temp)
                    if area > maxArea:
                        maxArea = area
                        ci = i
                res = contours1[ci]
                y1_max = frame.shape[0]-1
                for i in range(len(res)): #adjust offset on right hand + get top of hand coordinates
                    res[i][0][0]+=(frame.shape[1]*x_size)
                    if res[i][0][1] < y1_max:
                        y1_max = res[i][0][1]
                        x1_max = res[i][0][0]
                cv2.drawContours(frame, [res], 0, (0, 255, 0), 2)
                cv2.circle(frame, (x1_max, y1_max), 3, (0, 0, 255), 3)

                maxArea = -1
                if length2 > 0:
                    for i in range(length2):
                        temp = contours2[i]
                        area = cv2.contourArea(temp)
                        if area > maxArea:
                            maxArea = area
                            ci = i
                    res = contours2[ci]
                    y2_max = frame.shape[0]-1
                    for i in range(len(res)): # get top of hand coordinates for left hand
                        if res[i][0][1] < y2_max:
                            y2_max = res[i][0][1]
                            x2_max = res[i][0][0]
                    cv2.drawContours(frame, [res], 0, (0, 255, 0), 2) #draw contours
                    cv2.circle(frame, (x2_max, y2_max), 3, (0, 0, 255), 3) #draw top of hands


                # Display the resulting frame
        cv2.imshow('original', frame)

        if cv2.waitKey(1) == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

def findHandPos_frame(frame, bgModel=-1, x_size=0.5, threshold=60, draw_on_frame=True): #requires background model
    """finds the hand coordinates and contours for a single frame and a given background model"""
    y_size = 1

    frame = cv2.bilateralFilter(frame, 5, 50, 100)
    frame=cv2.flip(frame,1) #mirror webcam
    #draw rectange frame for right hand
    if draw_on_frame:
        cv2.rectangle(frame, (int(x_size * frame.shape[1]), 0),
                (frame.shape[1], int(y_size * frame.shape[0])), (255, 0, 0), 2) #<-- dis thing makes the fancy rectangle to put thou hand in.
        #draw rectange frame for left hand
        cv2.rectangle(frame, (int((x_size-0.003) * frame.shape[1]), 0),
                (0, int(y_size * frame.shape[0])), (0, 255, 0), 2) #<-- dis thing makes the fancy rectangle to put thou hand in.

    #  big boi calculations
    fgmask = bgModel.apply(frame,learningRate=0)
    kernel = np.ones((3, 3), np.uint8)
    fgmask = cv2.erode(fgmask, kernel, iterations=1)
    img = cv2.bitwise_and(frame, frame, mask=fgmask)
            #layout rectangular boundaries for each hand
    img1 = img[0:int(y_size * frame.shape[0]),
            int(x_size * frame.shape[1]):frame.shape[1]]
    img2 = img[0:int(y_size * frame.shape[0]),
            0:int(x_size * frame.shape[1])]
            
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    gray3 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur1 = cv2.GaussianBlur(gray1, (41, 41), 0) #<--blur boi 1
    blur2 = cv2.GaussianBlur(gray2, (41, 41), 0) #<--blur boi 2
    blur3 = cv2.GaussianBlur(gray3, (41, 41), 0) #<--blur boi 3 (combined 1 and 2)
    ret, thresh1 = cv2.threshold(blur1, threshold, 255, cv2.THRESH_BINARY)
    ret, thresh2 = cv2.threshold(blur2, threshold, 255, cv2.THRESH_BINARY)
    ret, thresh3 = cv2.threshold(blur3, threshold, 255, cv2.THRESH_BINARY)

            # once B&W image is created, find Countours
    contours1, hierarchy1 = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours2, hierarchy2 = cv2.findContours(thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    length1 = len(contours1)
    length2 = len(contours2)
    maxArea = -1
    if length1 > 0:
        for i in range(length1): #find contour area
            temp = contours1[i]
            area = cv2.contourArea(temp)
            if area > maxArea:
                maxArea = area
                ci = i
        res1 = contours1[ci]
        y1_max = frame.shape[0]-1
        for i in range(len(res1)): #adjust offset on right hand + get top of hand coordinates
            res1[i][0][0]+=(frame.shape[1]*x_size)
            if res1[i][0][1] < y1_max:
                y1_max = res1[i][0][1]
                x1_max = res1[i][0][0]
        if draw_on_frame:
            cv2.drawContours(frame, [res1], 0, (0, 255, 0), 2)
            cv2.circle(frame, (x1_max, y1_max), 3, (0, 0, 255), 3)

        maxArea = -1
        if length2 > 0:
            for i in range(length2):
                temp = contours2[i]
                area = cv2.contourArea(temp)
                if area > maxArea:
                    maxArea = area
                    ci = i
            res2 = contours2[ci]
            y2_max = frame.shape[0]-1
            for i in range(len(res2)): # get top of hand coordinates for left hand
                if res2[i][0][1] < y2_max:
                    y2_max = res2[i][0][1]
                    x2_max = res2[i][0][0]
            if draw_on_frame:
                cv2.drawContours(frame, [res2], 0, (0, 255, 0), 2) #draw contours
                cv2.circle(frame, (x2_max, y2_max), 3, (0, 0, 255), 3) #draw top of hands

    return frame, (x1_max, y1_max), (x2_max, y2_max), res1, res2