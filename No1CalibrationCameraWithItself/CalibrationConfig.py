import os
#需要先在vscode打开《CameraToRobot》这个文件夹
#读取当前***.py程序所在的路径
#这样换了运行文件夹，不用更改路径
py_path = os.path.abspath(os.path.dirname(__file__))

#相邻两个角点间的实际距离，单位cm
corners_length = 2.1

#木块边长3cm
square_length = 3


#标定棋盘大小, 列， 行, 指内角点个数，非棋盘格
calibration_size = (7, 7)


#采集标定图像存储路径
#save_path = '/home/pi/ArmPi/CameraCalibration/calibration_images/'
#save_path = 'D:\\Informations\\ArmPi\\191.ArmPi智能视觉机械臂\\5.附录\\2.源码\\ArmPi\\CameraCalibration\\calibration_images\\'
save_path = py_path + "\\calibration_images\\"


#标定参数存储的路径
#保存的文件名为：calibration_param.npz
#在《Calibration.py》计算出，并保存
#calibration_param_path = 'D:\\Informations\\ArmPi\\191.ArmPi智能视觉机械臂\\5.附录\\2.源码\\ArmPi\\CameraCalibration\\calibration_param'
calibration_param_path = py_path + "\\" + "calibration_param"


#映射参数存储路径
#保存的文件名为：map_param.npz
#在《GetMapParam.py》里面计算出，并保存
#map_param_path = '/home/pi/ArmPi/CameraCalibration/map_param'
#map_param_path = 'D:\\Informations\\ArmPi\\191.ArmPi智能视觉机械臂\\5.附录\\2.源码\\ArmPi\\CameraCalibration\\map_param'
map_param_path = py_path + "\\" + "map_param"