# -*- coding:utf-8 -*-
# 导入必要的软件包
import argparse
import datetime
import imutils
import time
import cv2
# 创建参数解析器并解析参数
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=80, help="minimum area size")
args = vars(ap.parse_args())
# 如果video参数为None，那么我们从摄像头读取数据
# camera = cv2.VideoCapture("C:\\Users\\epchy\\Desktop\\C\\test.mp4")
camera = cv2.VideoCapture("C:\\Users\\epchy\\Desktop\\河北省建模\\题目\\C题-运动目标的分割与检测研究\\附件\\附件2 小区红外视频.wmv")
# camera = cv2.VideoCapture(0)
# camera.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
# camera.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
# 初始化视频流的第一帧
firstFrame = None
# 遍历视频的每一帧
while True:
    # 获取当前帧并初始化occupied/unoccupied文本
    (grabbed, frame) = camera.read()
    ret,cc =camera.read()
    text = "Unoccupied"
    # 如果不能抓取到一帧，说明我们到了视频的结尾
    if not grabbed:
        break
    # 调整该帧的大小，转换为灰阶图像并且对其进行高斯模糊
    frame = imutils.resize(frame, width=700,height=600)
    cc = imutils.resize(cc, width=700,height=600)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    # 如果第一帧是None，对其进行初始化
    if firstFrame is None:
        firstFrame = gray
        continue
    print('ok')
    # 计算当前帧和第一帧的不同
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    print('ai')
    # 扩展阀值图像填充孔洞，然后找到阀值图像上的轮廓
    thresh = cv2.dilate(thresh, None, iterations=2)
    (_,cnts,_) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    # 遍历轮廓
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < args["min_area"]:
            continue
        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        # 计算轮廓的边界框，在当前帧中画出该框
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
        text = "Occupied"
    # draw the text and timestamp on the frame
    # 在当前帧上写文字以及时间戳
    # cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    # cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
    #             (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255),1)
    # 显示当前帧并记录用户是否按下按键
    cv2.imshow("Security Feed", frame)
    # cv2.imshow("Thresh", thresh)
    # cv2.imshow("Frame Delta", frameDelta)
    # cv2.imshow()
    cv2.imshow('image', cc)
    # amp = 0xFF
    # key = cv2.waitKey(1) & amp
    # # 如果q键被按下，跳出循环
    # if key == ord("q"):
    #     break
    # 处理按键效果
    key = cv2.waitKey(60) & 0xff
    if key == 27:  # 按下ESC时，退出
        break
    elif key == ord(' '):  # 按下空格键时，暂停
        cv2.waitKey(0)
    cv2.waitKey(0)
cv2.destroyAllWindows()
