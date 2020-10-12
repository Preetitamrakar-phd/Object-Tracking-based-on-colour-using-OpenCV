import imutils # for resizing
import cv2

#redLower(HueLower,SaturationLower,ValueLower)
redLower = (157,93,203)
redUpper = (179,255,255)
camera = cv2.VideoCapture(0) # initialize camera
while True:
    (grabbed, frame) = camera.read() #capture frame from the camera
    frame = imutils.resize(frame, width=600) # resizing small
    blurred = cv2.GaussianBlur(frame,(11,11),0) # smoothen image
    hsv = cv2.cvtColor(blurred,cv2.COLOR_BGR2HSV) #convert bgr to hsv

    mask = cv2.inRange(hsv,redLower,redUpper) #mask certain color which I want to track
    mask = cv2.erode(mask, None,iterations = 2) #to remove noise or holes
    mask = cv2.dilate(mask, None, iterations = 2)

    cnts = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE[-2])  
    center = None
    if len(cnts) > 0:
        c=max(cnts, key=cv2.contourArea)
        ((x,y),radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]),int(M["m01"]/M["m00"]))
        
        if radius > 10:
            cv2.circle(frame,(int(x), int(y)),int(radius),(0,0,255),2)
            cv2.circle(frame, center, 5, (0,0,255), -1)
            print(center[0], radius)
            if radius > 250:
                print("stop")
            else:
                if(center[0]<150):   #we require only x coordinate so center[0]
                    print("Left")
                elif(center[0]>450):
                    print("Right")
                elif(radius<250):
                    print("Front")
                else:
                    print("Stop")
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == odr("q"):
        break
camera.release()
cv2.destroyAllWindows()
        
                    
