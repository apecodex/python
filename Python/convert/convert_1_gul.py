from tkinter import *
from tkinter import messagebox
import math

class Convert_1():

	def __init__(self):
		self.mainwindows = Tk()
		ws = self.mainwindows.winfo_screenwidth()    # Get the monitor width
		hs = self.mainwindows.winfo_screenheight()    # Get the monitor height
		w = 600    # The width of the program
		h = 500    # The height of the program
		x = (ws / 2) - (w / 2)
		y = (hs / 2) - (h / 2)
		self.mainwindows.geometry("%dx%d+%d+%d" % (w, h, x, y))    # Centered
		self.mainwindows.title("")   # The title of the program,Is now empty,Please enter yourself
		# self.mainwindows.config(bg="#222")    # background

	def kiloToMiles(self,kilometers):

		# conversion factor
		conv_fac = 0.621371

		miles = float(kilometers) * conv_fac
		self.return_value_Text.delete(0.0, END)    # Empty the content
		self.return_value_Text.insert(END,'%0.3f kilometers is equal to %0.3f miles' % (kilometers, miles))    # Write content

	def celsiusToFahrenheit(self,Celsius):

		# conversion factor
		Fahrenheit = 9.0 / 5.0 * Celsius + 32

		self.return_value_Text.delete(0.0, END)    # Empty the content
		self.return_value_Text.insert(END,'%0.3f Celsius is equal to %0.3f Fahrenheit' % (Celsius, Fahrenheit))    # Write content

	def degreesToradians(self,degrees):

		# conversion factor
		radians = math.pi * degrees / 180

		self.return_value_Text.delete(0.0, END)    # Empty the content
		self.return_value_Text.insert(END,'%0.3f Degrees is equal to %0.3f Radians' % (degrees, radians))    # Write content

	def centimetersToinches(self,centimeters):

		# conversion factor
		inches = centimeters * 0.3937

		self.return_value_Text.delete(0.0, END)    # Empty the content
		self.return_value_Text.insert(END,'%0.3f Centimeters is equal to %0.3f inches' % (centimeters, inches))    # Write content

	def ConfirmtheCalculation(self):
		choose = self.var.get()
		user_input_value = self.Enter_Entry.get()
		if choose == 0:
			messagebox.showinfo(title="Remind",message="Please select an option")    # There is no choice of conversion button, jump out of the prompt
		elif user_input_value.strip() == "":
			messagebox.showinfo(title="Remind", message="Please enter the value to be converted")    # No input, jump out of the prompt box
		elif [value for value in user_input_value if value.isalpha()] != []:
			messagebox.showinfo(title="Remind", message="Please enter a number, not a string")    # The contents of the input string, jump out of the prompt box
		elif choose == 1:    # If selected Kilometres to Miles
			self.kiloToMiles(int(user_input_value))
		elif choose == 2:    # If selected Celsius to Fahrenheit
			self.celsiusToFahrenheit(int(user_input_value))
		elif choose == 3:    # If selected Degrees to Radians
			self.degreesToradians(int(user_input_value))
		elif choose == 4:    # If selected Centimeters to Inches
			self.centimetersToinches(int(user_input_value))
		else:
			pass  # Easy to expand


	def main(self):
		self.var = IntVar()    # Initialize options
		remind_label = Label(self.mainwindows,text="Select the button to convert",font=("宋体",25)).pack()
		KTM_btn = Radiobutton(self.mainwindows,text="Kilometres to Miles",variable=self.var,value=1,font=("宋体",15)).place(x=30,y=40)    # Kilometres to Miles Button
		CTF_btn = Radiobutton(self.mainwindows,text="Celsius to Fahrenheit",variable=self.var,value=2,font=("宋体",15)).place(x=30,y=70)    # Celsius to Fahrenheit Button
		DTR_btn = Radiobutton(self.mainwindows,text="Degrees to Radians",variable=self.var,value=3,font=("宋体",15)).place(x=350,y=40)    # Degrees to Radians Button
		CTI_btn = Radiobutton(self.mainwindows,text="Centimeters to Inches",variable=self.var,value=4,font=("宋体",15)).place(x=350,y=70)    # Centimeters to Inches Button
		Enter_label = Label(self.mainwindows,text="Enter Here: ",font=("宋体",20)).place(x=40,y=150)    # Enter the prompt
		self.Enter_Entry = Entry(self.mainwindows,font=("宋体",25))    # Enter the value of the conversion
		self.Enter_Entry.place(x=220,y=150)
		Entry_button = Button(self.mainwindows,text="Confirm the Calculation",font=("宋体",20),relief="solid",command=self.ConfirmtheCalculation).place(x=150,y=250)    # Confirm the Calculation Button
		self.return_value_Text = Text(self.mainwindows,width=34,height=4,font=("宋体",25),relief="solid")    # The value after conversion is output here
		self.return_value_Text.place(x=10,y=350)
		self.mainwindows.mainloop()    # while~


if __name__ == '__main__':
	convert = Convert_1()
	convert.main()