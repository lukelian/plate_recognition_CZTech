# -*- coding: utf-8 -*-

import cv2

cap = cv2.VideoCapture(0)                                        # 打开摄像头
print("VideoCapture is opened?", cap.isOpened())

ret, frame = cap.read()                                      # 读取摄像头图像
center = (frame.shape[1]//2, frame.shape[0]//2)              # 图像中心点位置

gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)               # 转灰度
cv2.circle(gray, center=center, radius=100, color=(0,0,255)) # 画圆
cv2.imwrite("capture.jpg", img)

cap.release()            # 释放摄像头