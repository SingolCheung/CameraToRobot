'''
这个程序的用途
读取并使用之前《1_Calibration_CameraWithSelf》相机标定——内参和外参的结果
打开相机
把读取的每一帧图像
经过反畸变以后
实时的显示出来
也就是
在cv2.imshow('img', img)显示的每一帧图像，是使用标定参数经过畸变处理后的图像
'''
#!/usr/bin/env python3
# encoding:utf-8
import os
#需要先在vscode打开《CameraToRobot》这个文件夹
#读取当前***.py程序所在的路径
#这样换了运行文件夹，不用更改路径
py_path = os.path.abspath(os.path.dirname(__file__))
import sys
#sys.path.append('D:\\Informations\\ArmPi\\191.ArmPi智能视觉机械臂\\5.附录\\2.源码\\ArmPi')
#sys.path.append('/home/pi/ArmPi/')
sys.path.append('d:\\Informations\\VScode\\CameraToRobot')
import cv2
import time
import threading
import numpy as np
from No1CalibrationCameraWithItself.CalibrationConfig import *

if sys.version_info.major == 2:
    print('Please run this program with python3!')
    sys.exit(0)

#摄像头标定教程和解释
#https://www.jianshu.com/p/df78749b4318

class Camera:
    def __init__(self, resolution=(640, 480)):
        self.cap = None
        self.width = resolution[0]
        self.height = resolution[1]
        self.frame = None
        self.opened = False
        self.NoVideoCapture = 0
        
        #加载参数
        self.param_data = np.load(calibration_param_path + '.npz')
        '''
        for i in self.param_data:
            print("i=",i)
        '''
        #获取参数
        self.mtx = self.param_data['mtx_array']
        self.dist = self.param_data['dist_array']
        #self.fmt = self.param_data['fmt']
        #self.delimiter = self.param_data['delimiter']
        self.newcameramtx, roi = cv2.getOptimalNewCameraMatrix(self.mtx, self.dist, (self.width, self.height), 0, (self.width, self.height))
        #函数功能：计算无畸变和修正转换映射
        #https://blog.csdn.net/u013341645/article/details/78710740
        self.mapx, self.mapy = cv2.initUndistortRectifyMap(self.mtx, self.dist, None, self.newcameramtx, (self.width,self.height), 5)
        
        self.th = threading.Thread(target=self.camera_task, args=(), daemon=True)
        self.th.start()

    def camera_open(self):
        try:
            #把程序从树莓派拷贝到win10下，把cv2.VideoCapture(-1)更改为cv2.VideoCapture(self.NoVideoCapture)
            #self.cap = cv2.VideoCapture(-1)
            self.cap = cv2.VideoCapture(self.NoVideoCapture)
            self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y', 'U', 'Y', 'V'))
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            self.cap.set(cv2.CAP_PROP_SATURATION, 40)
            self.opened = True
        except Exception as e:
            print('打开摄像头失败:', e)

    def camera_close(self):
        try:
            self.opened = False
            time.sleep(0.2)
            if self.cap is not None:
                self.cap.release()
                time.sleep(0.05)
            self.cap = None
        except Exception as e:
            print('关闭摄像头失败:', e)

    def camera_task(self):
        while True:
            try:
                if self.opened and self.cap.isOpened():
                    ret, frame_tmp = self.cap.read()
                    if ret:
                        frame_resize = cv2.resize(frame_tmp, (self.width, self.height), interpolation = cv2.INTER_NEAREST)
                        self.frame = cv2.remap(frame_resize, self.mapx, self.mapy, cv2.INTER_LINEAR)
                    else:
                        #print(1)
                        self.frame = None
                        #cap = cv2.VideoCapture(-1)
                        cap = cv2.VideoCapture(self.NoVideoCapture)
                        ret, _ = cap.read()
                        if ret:
                            self.cap = cap
                elif self.opened:
                    #cap = cv2.VideoCapture(-1)
                    cap = cv2.VideoCapture(self.NoVideoCapture)
                    ret, _ = cap.read()
                    if ret:
                        self.cap = cap
                else:
                    time.sleep(0.01)
            except Exception as e:
                print('获取摄像头画面出错:', e)
                time.sleep(0.01)

if __name__ == '__main__':
    my_camera = Camera()
    my_camera.camera_open()
    while True:
        img = my_camera.frame
        if img is not None:
            cv2.imshow('img', img)
            key = cv2.waitKey(1)
            if key == 27:
                break
    my_camera.camera_close()
    cv2.destroyAllWindows()
