import numpy as np
import cv2

lower = np.array([0,137,60],np.uint8)
upper = np.array([255,180,127],np.uint8)
x_initial,h_initial,y_initial,w_initial=300,200,100,150
start_tracking = False

cap = cv2.VideoCapture(0)
cap.set(3,640); cap.set(4,480)
cap.set(cv2.CAP_PROP_FPS, 20)

prev_x, prev_y, SENSITIVITY = 0, 0, 12

while True:
    _,frame = cap.read()

    if not start_tracking:
        x,y,w,h = x_initial, y_initial, w_initial, h_initial
        
        display = cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
        display = cv2.putText(display, "Place your hand here. Then Press 's'", (x-30,y-10), cv2.FONT_HERSHEY_PLAIN,1,(0,0,0),thickness=1)
        cv2.imshow('Place your hand into the window',display)

        # set up the ROI for tracking
        track_window = (x,y,w,h)
        roi = frame[y:y+h, x:x+w]
        cv2.imshow('ROI',roi)
        hsv_roi =  cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
        roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
        cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

        # Setup the termination criteria, either 10 iteration or move by atleast 1 pt
        term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
    else:
        print('                                                                                                                                          \r',end='')
        try:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)

            # apply meanshift to get the new location
            ret, track_window = cv2.CamShift(dst, track_window, term_crit)

            # Draw it on image
            x,y,w,h = track_window

            roi = frame[y:y+h, x:x+w]
            ycrcb = cv2.cvtColor(roi,cv2.COLOR_BGR2YCR_CB)

            #Create a binary image with where white will be skin colors and rest is black
            mask = cv2.inRange(ycrcb,lower,upper)
            skin = cv2.bitwise_and(roi, roi, mask = mask)
            ret,thresh = cv2.threshold(mask,127,255,0)

            
            #Find contours of the filtered frame
            _,contours,_ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

            length = len(contours)
            maxArea = -1
            if length > 0:
                for i in range(length):  # find the biggest contour (according to area)
                    temp = contours[i]
                    area = cv2.contourArea(temp)
                    if area > maxArea:
                        maxArea = area
                        ci = i

                res = contours[ci]
                hull = cv2.convexHull(res)
                x1,y1,w1,h1 = cv2.boundingRect(res)
                x+=x1;y+=y1
                #h1+=20;w1+=20
                track_window = (x,y,w1,h1)


            contoured_thresh = np.zeros(roi.shape, np.uint8)
            cv2.drawContours(contoured_thresh, [res], 0, (0, 255, 0), 2)
            cv2.drawContours(contoured_thresh, [hull], 0, (0, 255, 0), 2)
            #cv2.imshow('ROI with contours',contoured_thresh)

            (cx,cy),(major_axis,minor_axis),angle = cv2.fitEllipse(res)
            cx += x; cy += y
            cv2.ellipse(frame,(int(cx),int(cy)),(int(major_axis/2),int(minor_axis/2)),int(angle),0,360,(0,255,0),thickness=2)

            delta_x, delta_y, slope, direction = prev_x-cx, prev_y-cy, 0, 'No movement'

            if delta_x**2+delta_y**2 > SENSITIVITY**2:
                if delta_x is 0 and delta_y > 0: slope = 999 # inf
                elif delta_x is 0 and delta_y < 0: slope = -999 # -inf
                else: slope = float(delta_y/delta_x)

                if slope < 0.5 and slope > -0.5 and delta_x > 0: direction = 'East'
                elif slope <= 2.0 and slope >= 0.5 and delta_x > 0 and delta_y > 0: direction = 'North-East'
                elif slope >= -2.0 and slope <= -0.5 and delta_x < 0 and delta_y > 0: direction = 'North-West'
                elif slope >= -2.0 and slope <= -0.5 and delta_x > 0 and delta_y < 0: direction = 'South-East'
                elif slope <= 2.0 and slope >= 0.5 and delta_x < 0 and delta_y < 0: direction = 'South-West'
                elif slope < 0.5 and slope > -0.5: direction = 'West'
                elif (slope > 2.0 or slope < -2.0) and delta_y > 0.0: direction = 'North'
                elif slope > 2.0 or slope < -2.0: direction = 'South'

                SENSITIVITY = 7
                prev_x, prev_y = cx, cy
            else:
                direction = 'No movement'
                SENSITIVITY = 12
            
            cv2.putText(frame, direction, (25,25), cv2.FONT_HERSHEY_PLAIN, 2, (0,0,0), thickness=2)
            cv2.imshow('Hand tracking',frame)
            #cv2.imshow('Segmented',skin)
            print('Slope = '+str(round(slope,3))+'\tDirection = '+str(direction)+'\r', end='')
        except Exception as e:
            print(e)
            frame = cv2.putText(frame,'Check terminal for error',(25,25),cv2.FONT_HERSHEY_PLAIN,2,(0,0,0),thickness=2)
            cv2.imshow('Tracking',frame)
    k = cv2.waitKey(100) & 0xff
    if k == ord('q'):
        break
    elif k==ord('s'):
        start_tracking=not start_tracking
        cv2.destroyAllWindows()

cv2.destroyAllWindows()
cap.release()