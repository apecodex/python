from tkinter import *
from tkinter import messagebox
import math
import threading

class Convert():

	def __init__(self):
		self.mainwindows = Tk()
		self.mainwindows.wm_attributes('-topmost', 1)
		ws = self.mainwindows.winfo_screenwidth()    # Get the monitor width
		hs = self.mainwindows.winfo_screenheight()    # Get the monitor height
		w = 210    # The width of the program
		h = 200    # The height of the program
		x = (ws / 4) - (w / 2)
		y = (hs / 2) - (h / 2)
		self.mainwindows.geometry("%dx%d+%d+%d" % (w, h, x, y))    # Centered
		self.mainwindows.maxsize("210", "200")
		self.mainwindows.minsize("210", "200")
		self.mainwindows.title("")   # The title of the program,Is now empty,Please enter yourself
		# self.mainwindows.config(bg="#222")    # background

	def triangle(self,a,b,c):

		s = (a + b + c) / 2

		area = (s * (s - a) * (s - b) * (s - c)) ** 0.5

		try:
			self.triangle_values.set('The area of the triangle is %0.2f' % area)
		except TypeError:
			self.triangle_values.set("Can't convert complex to float")

	def rectangle(self,a,b):

		area = a * b

		self.rectangle_values_text.delete(0.0,END)
		self.rectangle_values_text.insert(END,'The area of the rectangle is %0.3f' % area)

	def circle(self,r):

		# conversion factor
		area = math.pi * r * r

		self.circle_values_text.delete(0.0,END)
		self.circle_values_text.insert(END,'The area of the circle is %0.3f' % area)

	def trapezoids(self,base1,base2,height):

		Area = 0.5 * (base1 + base2) * height

		self.trapezoids_values_text.delete(0.0, END)
		self.trapezoids_values_text.insert(END, "Area of a Trapezium = %.3f " % Area)

	def Areaoftriangle_function(self):
		first_side_value = self.first_side_Entry.get()    # Get value
		second_side_value = self.second_side_Entry.get()
		third_side_value = self.third_side_Entry.get()
		if first_side_value.strip == "":    # No input, jump out of the prompt box
			messagebox.showinfo(title="Remind", message="The value can not be empty")
		elif second_side_value.strip == "":    # No input, jump out of the prompt box
			messagebox.showinfo(title="Remind", message="The value can not be empty")
		elif third_side_value.strip() == "":    # No input, jump out of the prompt box
			messagebox.showinfo(title="Remind",message="The value can not be empty")
		elif [value for value in first_side_value if value.isalpha()] != [] or [value for value in second_side_value if value.isalpha()] != [] or [value for value in third_side_value if value.isalpha()] != []:     # The contents of the input string, jump out of the prompt box
			messagebox.showinfo(title="Remind", message="Please enter a number, not a string")
		else:
			a = float(first_side_value)
			b = float(second_side_value)
			c = float(third_side_value)
			self.triangle(a,b,c)

	def Areaofrectangle_function(self):
		lengthofsideA_value = self.lengthofsideA_Entry.get()    # Get value
		lengthofsideB_value = self.lengthofsideB_Entry.get()    # Get value
		if lengthofsideA_value.strip == "":
			messagebox.showinfo(title="Remind", message="The value can not be empty")
		elif lengthofsideB_value.strip == "":
			messagebox.showinfo(title="Remind", message="The value can not be empty")
		elif [value for value in lengthofsideA_value if value.isalpha()] != [] or [value for value in lengthofsideB_value if value.isalpha()] != []:
			messagebox.showinfo(title="Remind", message="Please enter a number, not a string")
		else:
			try:
				a = float(lengthofsideA_value)
				b = float(lengthofsideB_value)
				self.rectangle(a, b)
			except ValueError:
				messagebox.showinfo(title="Remind", message="Check whether the input box has entered the content?")

	def Areaofcircle_function(self):
		radiusofthecircle_Entry = self.radiusofthecircle_Entry.get()
		if radiusofthecircle_Entry.strip == "":
			messagebox.showinfo(title="Remind", message="The value can not be empty")
		elif [value for value in radiusofthecircle_Entry if value.isalpha()] != []:
			messagebox.showinfo(title="Remind", message="Please enter a number, not a string")
		else:
			try:
				r = float(radiusofthecircle_Entry)
				self.circle(r)
			except ValueError:
				messagebox.showinfo(title="Remind", message="Check whether the input box has entered the content?")

	def Areaoftrapezoids_function(self):
		First_Base_of_a_Trapezoid_Value = self.First_Base_of_a_Trapezoid_Entry.get()
		Second_Base_of_a_Trapezoid_Value = self.Second_Base_of_a_Trapezoid_Entry.get()
		Height_of_a_Trapezoid_Value = self.Height_of_a_Trapezoid_Entry.get()
		if First_Base_of_a_Trapezoid_Value.strip == "":
			messagebox.showinfo(title="Remind", message="The value can not be empty")
		elif Second_Base_of_a_Trapezoid_Value.strip == "":
			messagebox.showinfo(title="Remind", message="The value can not be empty")
		elif Height_of_a_Trapezoid_Value.strip() == "":
			messagebox.showinfo(title="Remind",message="The value can not be empty")
		elif [value for value in First_Base_of_a_Trapezoid_Value if value.isalpha()] != [] or [value for value in Second_Base_of_a_Trapezoid_Value if value.isalpha()] != [] or [value for value in Height_of_a_Trapezoid_Value if value.isalpha()] != []:
			messagebox.showinfo(title="Remind", message="Please enter a number, not a string")
		else:
			try:
				base1 = float(First_Base_of_a_Trapezoid_Value)
				base2 = float(Second_Base_of_a_Trapezoid_Value)
				height = float(Height_of_a_Trapezoid_Value)
				self.trapezoids(base1,base2,height)
			except ValueError:
				messagebox.showinfo(title="Remind", message="Check whether the input box has entered the content?")

	def Areaoftriangle_windows(self):
		self.trianglewindows = Toplevel(self.mainwindows)
		self.trianglewindows.wm_attributes('-topmost', 1)    # Top
		ws = self.trianglewindows.winfo_screenwidth()    # Get the monitor width
		hs = self.trianglewindows.winfo_screenheight()    # Get the monitor height
		w = 400    # The width of the program
		h = 300    # The height of the program
		x = (ws / 2) - (w / 2)
		y = (hs / 2) - (h / 2)
		self.trianglewindows.geometry("%dx%d+%d+%d" % (w, h, x, y))    # Centered
		self.trianglewindows.maxsize("400", "300")
		self.trianglewindows.minsize("400", "300")
		self.trianglewindows.title("Triangle")   # title
		# self.trianglewindows.config(bg="#222")
		self.triangle_values = StringVar()
		self.triangle_values.set("null")
		first_side_label = Label(self.trianglewindows,text="Enter first side: ",font=("宋体",15)).place(x=10,y=10)
		second_side_label = Label(self.trianglewindows,text="Enter second side: ",font=("宋体",15)).place(x=10,y=60)
		third_side_label = Label(self.trianglewindows,text="Enter third side: ",font=("宋体",15)).place(x=10,y=110)
		rectangle_label = Label(self.trianglewindows, text="Area of triangle", font=("宋体", 20),fg="red",relief="flat").place(x=10, y=180)
		self.first_side_Entry = Entry(self.trianglewindows,font=("宋体",20),width=13)
		self.first_side_Entry.place(x=200,y=10)
		self.second_side_Entry = Entry(self.trianglewindows,font=("宋体",20),width=13)
		self.second_side_Entry.place(x=200,y=60)
		self.third_side_Entry = Entry(self.trianglewindows,font=("宋体",20),width=13)
		self.third_side_Entry.place(x=200,y=110)
		Enter_button = Button(self.trianglewindows,text="Calculation",font=("宋体",15),command=self.Areaoftriangle_function).place(x=250,y=180)
		values_label = Label(self.trianglewindows,textvariable=self.triangle_values,font=("宋体",15)).place(x=10,y=250)


	def Areaofrectangle_windows(self):
		self.rectanglewindows = Toplevel(self.mainwindows)
		self.rectanglewindows.wm_attributes('-topmost', 1)    # Top
		ws = self.rectanglewindows.winfo_screenwidth()    # Get the monitor width
		hs = self.rectanglewindows.winfo_screenheight()    # Get the monitor height
		w = 450    # The width of the program
		h = 300    # The height of the program
		x = (ws / 2) - (w / 2)
		y = (hs / 2) - (h / 2)
		self.rectanglewindows.geometry("%dx%d+%d+%d" % (w, h, x, y))    # Centered
		self.rectanglewindows.maxsize("450", "300")
		self.rectanglewindows.minsize("450", "300")
		self.rectanglewindows.title("Rectangle")    # title
		# self.rectanglewindows.config(bg="#222")

		lengthofsideA_label = Label(self.rectanglewindows,text="Enter first side: ",font=("宋体",15)).place(x=10,y=10)
		lengthofsideB_label = Label(self.rectanglewindows,text="Enter second side: ",font=("宋体",15)).place(x=10,y=60)
		rectangle_label = Label(self.rectanglewindows, text="Area of rectangle", font=("宋体", 20), fg="red",relief="flat").place(x=10, y=120)
		self.lengthofsideA_Entry = Entry(self.rectanglewindows,font=("宋体",20),width=16)
		self.lengthofsideA_Entry.place(x=200,y=10)
		self.lengthofsideB_Entry = Entry(self.rectanglewindows,font=("宋体",20),width=16)
		self.lengthofsideB_Entry.place(x=200,y=60)
		Enter_button = Button(self.rectanglewindows, text="Calculation", font=("宋体", 15), command=self.Areaofrectangle_function).place(x=300, y=120)
		self.rectangle_values_text = Text(self.rectanglewindows,font=("宋体", 15),width=43,height=3)
		self.rectangle_values_text.place(x=10, y=230)


	def Areaofcircle_windows(self):
		self.circlewindows = Toplevel(self.mainwindows)
		self.circlewindows.wm_attributes('-topmost', 1)    # Top
		ws = self.circlewindows.winfo_screenwidth()    # Get the monitor width
		hs = self.circlewindows.winfo_screenheight()    # Get the monitor height
		w = 520    # The width of the program
		h = 250    # The height of the program
		x = (ws / 2) - (w / 2)
		y = (hs / 2) - (h / 2)
		self.circlewindows.geometry("%dx%d+%d+%d" % (w, h, x, y))    # Centered
		self.circlewindows.maxsize("520", "250")
		self.circlewindows.minsize("520", "250")
		self.circlewindows.title("Circle")    # title
		# self.circlewindows.config(bg="#222")

		radius_of_the_circle_label = Label(self.circlewindows,text="Enter radius of the circle: ",font=("宋体",15),).place(x=10,y=10)
		circle_label = Label(self.circlewindows, text="Area of circle", font=("宋体", 20),fg="red", relief="flat").place(x=10, y=80)
		self.radiusofthecircle_Entry = Entry(self.circlewindows, font=("宋体", 20), width=16)
		self.radiusofthecircle_Entry.place(x=285,y=10)
		Enter_button = Button(self.circlewindows, text="Calculation", font=("宋体", 15), command=self.Areaofcircle_function).place(x=380, y=80)
		self.circle_values_text = Text(self.circlewindows, font=("宋体", 15), width=50, height=3)
		self.circle_values_text.place(x=10, y=180)


	def Areaoftrapezoids_windows(self):
		self.trapezoidswindows = Toplevel(self.mainwindows)
		self.trapezoidswindows.wm_attributes('-topmost', 1)    # Top
		ws = self.trapezoidswindows.winfo_screenwidth()    # Get the monitor width
		hs = self.trapezoidswindows.winfo_screenheight()    # Get the monitor height
		w = 500    # The width of the program
		h = 330    # The height of the program
		x = (ws / 2) - (w / 2)
		y = (hs / 2) - (h / 2)
		self.trapezoidswindows.geometry("%dx%d+%d+%d" % (w, h, x, y))    # Centered
		self.trapezoidswindows.maxsize("500", "330")
		self.trapezoidswindows.minsize("500", "330")
		self.trapezoidswindows.title("trapezoids")   # title
		# self.trapezoidswindows.config(bg="#222")

		First_Base_of_a_Trapezoid_label = Label(self.trapezoidswindows,text="First Base of a Trapezoid: ",font=("宋体",15)).place(x=10,y=10)
		Second_Base_of_a_Trapezoid_label = Label(self.trapezoidswindows,text="Second Base of a Trapezoid: ",font=("宋体",15)).place(x=10,y=60)
		Height_of_a_Trapezoid_label = Label(self.trapezoidswindows,text="Height of a Trapezoid: ",font=("宋体",15)).place(x=10,y=110)
		trapezoids_label = Label(self.trapezoidswindows,text="Area of trapezoids",font=("宋体",20),fg="red",relief="flat").place(x=10,y=180)
		self.First_Base_of_a_Trapezoid_Entry = Entry(self.trapezoidswindows,font=("宋体",20),width=15)
		self.First_Base_of_a_Trapezoid_Entry.place(x=280,y=10)
		self.Second_Base_of_a_Trapezoid_Entry = Entry(self.trapezoidswindows,font=("宋体",20),width=15)
		self.Second_Base_of_a_Trapezoid_Entry.place(x=280,y=60)
		self.Height_of_a_Trapezoid_Entry = Entry(self.trapezoidswindows,font=("宋体",20),width=15)
		self.Height_of_a_Trapezoid_Entry.place(x=280,y=110)
		Enter_button = Button(self.trapezoidswindows,text="Calculation",font=("宋体",15),command=self.Areaoftrapezoids_function).place(x=330,y=180)
		self.trapezoids_values_text = Text(self.trapezoidswindows,font=("宋体", 15), width=47, height=3)
		self.trapezoids_values_text.place(x=10, y=250)


	#    Increase thread to prevent suspended animation
	def Areaoftriangle_threading(self,):
		th = threading.Thread(target=self.Areaoftriangle_windows)
		th.setDaemon(True)
		th.start()

	def Areaofrectangle_threading(self):
		th = threading.Thread(target=self.Areaofrectangle_windows)
		th.setDaemon(True)
		th.start()

	def Areaofcircle_threading(self):
		th = threading.Thread(target=self.Areaofcircle_windows)
		th.setDaemon(True)
		th.start()

	def Areaoftrapezoids_threading(self):
		th = threading.Thread(target=self.Areaoftrapezoids_windows)
		th.setDaemon(True)
		th.start()

	def main(self):
		Areaoftriangle = Button(self.mainwindows,text="Area of triangle",font=("宋体",15),command=self.Areaoftriangle_threading).place(x=10,y=10)
		Areaofrectangle = Button(self.mainwindows,text="Area of rectangle",font=("宋体",15),command=self.Areaofrectangle_threading).place(x=10,y=60)
		Areaofcircle = Button(self.mainwindows,text="Area of circle",font=("宋体",15),command=self.Areaofcircle_threading).place(x=10,y=110)
		Areaoftrapezoids = Button(self.mainwindows,text="Area of trapezoids",font=("宋体",15),command=self.Areaoftrapezoids_threading).place(x=10,y=160)
		self.mainwindows.mainloop()    # while~


if __name__ == '__main__':
	convert = Convert()
	convert.main()