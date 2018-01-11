import os
import PIL
import time
import numpy
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Wechat_jump():

	def __init__(self):
		self.need_update = True

	# 获取图片/界面
	def get_screen_image(self):
		os.system("adb shell screencap -p /sdcard/screen.png")    # 获取当前手机截图
		os.system("adb pull /sdcard/screen.png")    # 从手机里获取图片并保存到电脑当前本地文件夹
		return numpy.array(PIL.Image.open("screen.png"))    # 返回一个二维数组

	# 计算玄
	def jump_to_next(self,point1,point2):
		x1, y1 = point1    # 起点位置的X轴和Y轴
		x2, y2 = point2    # 终点位置的X轴和Y轴
		tan = ((x2 - x1)**2 + (y2 - y1)**2)**0.5    # 通过勾股定理计算起点坐标到终点坐标的长度
		os.system("adb shell input swipe 320 410 320 410 {}".format(int(tan*1.35)))    # 按压的时间，320 410的意思就是手指点在手机屏幕上的位置

	# 鼠标单击回调
	def on_calck(self,event, coor=[]):
		coor.append((event.xdata,event.ydata))    # 获取鼠标单击的X轴和Y轴
		if len(coor) == 2:   # 判断列表里的元素有没有两个，一个是起点位置的X轴和Y轴，另一个是终点位置的X轴和Y轴
			print("起点位置: {} 结束位置: {}".format(event.xdata,event.ydata))
			self.jump_to_next(coor.pop(),coor.pop())    # 将起点位置和终点位置的坐标轴计算长度
			self.need_update = True

	# 更新图片
	def update_screen(self,frame):
		if self.need_update:
			time.sleep(1)
			self.axes_image.set_array(self.get_screen_image())    # 重新获取图片
			self.need_update = False
		return self.axes_image,    # 返回元组类型

	def main(self):
		figure = plt.figure()    # 创建一张空白的图片
		self.axes_image = plt.imshow(self.get_screen_image(),animated=True)    #把获取的图片放在坐标轴上~
		figure.canvas.mpl_connect("button_press_event",self.on_calck)    # 绑定鼠标单击事件
		ani = FuncAnimation(figure,self.update_screen,interval=50,blit=True)    # 刷新图片
		plt.show()    # 显示

if __name__ == '__main__':
	w = Wechat_jump()
	w.main()