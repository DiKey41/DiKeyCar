import numpy as np
import cv2


cap = cv2.VideoCapture(0)
noDrive=cv2.imread("noDrive.jpeg")
right=cv2.imread("right.jpeg")
left=cv2.imread("left.jpeg")
forward=cv2.imread("forward.jpeg")
forwardleft=cv2.imread("forwardleft.jpeg")
forwardright=cv2.imread("forwardright.jpeg")
noDrive=cv2.resize(noDrive,(64,64))
right=cv2.resize(right,(64,64))
left=cv2.resize(left,(64,64))
forward=cv2.resize(forward,(64,64))
forwardright=cv2.resize(forwardright,(64,64))
forwardleft=cv2.resize(forwardleft,(64,64))

noDrive=cv2.inRange(noDrive,(89,91,149),(255,255,255))
right=cv2.inRange(right,(89,91,149),(255,255,255))
left=cv2.inRange(left,(89,91,149),(255,255,255))
forward=cv2.inRange(forward,(89,91,149),(255,255,255))
forwardright=cv2.inRange(forwardright,(89,91,149),(255,255,255))
forwardleft=cv2.inRange(forwardleft,(89,91,149),(255,255,255))


#Отображение знаков 
#cv2.imshow('noDrive',noDrive)
#cv2.imshow('right',right)
#cv2.imshow('left',left)
#cv2.imshow('forward',forward)
#cv2.imshow('forwardleft',forwardleft)
#cv2.imshow('forwardright',forwardright)

while(True):
    ret, frame = cap.read()
    #cv2.imshow('Frame',frame)
    frameCopy=frame.copy()
    
    
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    hsv = cv2.blur(hsv,(5,5))
    mask = cv2.inRange(hsv,(89,124,73),(255,255,255))
    #cv2.imshow('Mask',mask)


    mask=cv2.erode(mask, None, iterations = 2)
    mask=cv2.dilate(mask, None, iterations = 4)
    cv2.imshow('Mask2',mask)
    
    
    
    contours = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    contours = contours[0]
    if contours:
        contours = sorted(contours,key=cv2.contourArea,reverse=True)
        cv2.drawContours(frame,contours,0,(255,0,255),3)
        #cv2.imshow('Contours',frame)
    
        (x,y,w,h) = cv2.boundingRect(contours[0])
        cv2.rectangle(frame,(x,y),((x+w),(y+h)),(0,255,0),2)
        cv2.imshow('Rectangle',frame)
        
        roImg=frameCopy[y:y+h,x:x+w]
        cv2.imshow('Detect',roImg)
        roImg=cv2.resize(roImg,(64,64))
        roImg=cv2.inRange(roImg,(89,124,73),(255,255,255))
        cv2.imshow("resizeDetect",roImg)
        
        noDrive_val=0
        forward_val=0
        left_val=0
        right_val=0
        forwardleft_val=0
        forwardright_val=0
        
        
        for i in range(64):
            for j in range(64):
                if roImg[i][j]==noDrive[i][j]:
                    noDrive_val+=1
                if roImg[i][j]==forward[i][j]:
                    forward_val+=1
                if roImg[i][j]==forwardleft[i][j]:
                    forwardleft_val+=1
                if roImg[i][j]==forwardright[i][j]:
                    forwardright_val+=1
                if roImg[i][j]==left[i][j]:
                    left_val+=1
                if roImg[i][j]==right[i][j]:
                    right_val+=1
                    
      #  print('noDrive: ',noDrive_val)
        print('forward: ',forward_val)
      #  print('left: ',left_val)
      #  print('right: ',right_val)
        print('forward left: ',forwardleft_val)
      #  print('forward right: ',forwardright_val)
                
        if noDrive_val>2700:
           print('noDrive')
        elif forward_val>3400:
            print('forward')
        elif left_val>3400:
            print('left')
        elif right_val>3050:
            print('right')
        elif forwardleft_val>2400:
            print('forward left')
        elif forwardright_val>2500:
            print('forward right')
        else: print('nothing')
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
