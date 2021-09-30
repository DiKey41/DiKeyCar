import numpy as np
import cv2


cap = cv2.VideoCapture(0)

src = np.float32([[100,200],
                  [340,200],
                  [285,60],
                  [185,60]])

src_draw=np.array(src,dtype=np.int32)

dst = np.float32([[0,480],
                 [360,480],
                 [360,0],
                 [0,0]])

while(True):
    ret, frame = cap.read()
    cv2.imshow('Frame',frame)
    frameCopy=frame.copy()
    
    resized=cv2.resize(frame,(480,320))
    
   # cv2.imshow('frame',resized)

    r_channel=resized[:,:,2]
    binary = np.zeros_like(r_channel)
    binary[(r_channel>100)]=1
    #cv2.imshow('binary',binary)
    
    hls=cv2.cvtColor(resized,cv2.COLOR_BGR2HLS)
    s_channel=resized[:,:,2]
    binary2=np.zeros_like(s_channel)
    binary2[(s_channel)>80]=1


    allbinary = np.zeros_like(binary)
    allbinary[((binary==1)|(binary2==1))]=255
    #cv2.imshow('allbinary',allbinary)
    
    allbinary_visual=allbinary.copy()
    cv2.polylines(allbinary_visual,[src_draw],True,255)
    #cv2.imshow('polygon',allbinary_visual)
    allbinary=cv2.bitwise_not(allbinary)
    
    M=cv2.getPerspectiveTransform(src,dst)
    warped = cv2.warpPerspective(allbinary,M,(480,480),flags=cv2.INTER_LINEAR)
  #  cv2.imshow('warped',warped)
    cv2.imshow('warped',warped)
    
    
    
    histogram=np.sum(warped[warped.shape[0]//2:,:],axis=0)
    midpoint=histogram.shape[0]//2
    #IndWhitestColumnL = np.argmax(histogram[:midpoint])
    IndWhitestColumnR = np.argmax(histogram)
    warped_visual=warped.copy()
    #cv2.line(warped_visual,(IndWhitestColumnL,0),(IndWhitestColumnL,warped_visual.shape[0]),110,2)
    cv2.line(warped_visual,(IndWhitestColumnR,0),(IndWhitestColumnR,warped_visual.shape[0]),110,2)
    #cv2.imshow('whitest',warped_visual)

    nwindows=10
    window_height=np.int_(warped.shape[0]/nwindows)
    window_half_width=25
    
    XCenterWindow = IndWhitestColumnR
    center_lane_inds = np.array([],dtype=np.int16)

    out_img=np.dstack((warped,warped,warped))
    
    
    nonzero= warped.nonzero()
    WhitePixelIndY=np.array(nonzero[0])
    WhitePixelIndX=np.array(nonzero[1])

    for window in range(nwindows):
        win_y1 = warped.shape[0] - (window+1)*window_height
        win_y2 = warped.shape[0] - (window)*window_height
        
        center_win_x1=XCenterWindow-window_half_width
        center_win_x2=XCenterWindow+window_half_width
            
        cv2.rectangle(out_img,(center_win_x1,win_y1),(center_win_x2,win_y2),(50+window*21,0,0),2)
        cv2.imshow('windows',out_img)
        
        good_center_inds = ((WhitePixelIndY>=win_y1) & (WhitePixelIndY<=win_y2)
         &(WhitePixelIndX>=center_win_x1)&(WhitePixelIndX<=center_win_x2)).nonzero()[0]
        
        center_lane_inds = np.concatenate((center_lane_inds,good_center_inds))
        if len(good_center_inds) > 5:
            XCenterWindow = np.int_(np.mean(WhitePixelIndX[good_center_inds]))
        
        
    out_img[WhitePixelIndY[center_lane_inds],WhitePixelIndX[center_lane_inds]] = [255,0,0]
    cv2.imshow("Lane",out_img)
    
    centralx=WhitePixelIndX[center_lane_inds]
    centraly=WhitePixelIndY[center_lane_inds]
    
    if centralx[0]<200:
        print('left')
    elif centralx[0]>280:
        print('right')
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
