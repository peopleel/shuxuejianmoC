# encoding: UTF-8
import glob as gb
import cv2

img_path = gb.glob("C:\\Users\\epchy\\Desktop\\河北省建模\\题目\\C题-运动目标的分割与检测研究\\附件\\附件1 图像序列\\*.bmp")
videoWriter = cv2.VideoWriter('test1.avi', cv2.VideoWriter_fourcc(*'MJPG'), 15, (640,480))

for path in img_path:
    img  = cv2.imread(path)
    img = cv2.resize(img,(640,480))
    videoWriter.write(img)
