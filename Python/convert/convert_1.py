# Convert Kilometres to Miles, Convert Celsius to Fahrenheit, convert degrees to radians, convert to inches.


# Kilometres to Miles

import math


def kiloToMiles():

    kilometers = float(input("Enter value in kilometers"))

    # conversion factor
    conv_fac = 0.621371

    miles = kilometers * conv_fac
    print('%0.3f kilometers is equal to %0.3f miles' % (kilometers, miles))


def celsiusToFahrenheit():

    Celsius = float(input("Enter value in Celsius"))

    # conversion factor
    Fahrenheit = 9.0 / 5.0 * Celsius + 32

    print('%0.3f Celsius is equal to %0.3f Fahrenheit' % (Celsius, Fahrenheit))


def degreesToradians():

    degrees = float(input("Enter value in degrees"))

    # conversion factor
    radians = math.pi * degrees / 180

    print('%0.3f Degrees is equal to %0.3f Radians' % (degrees, radians))


def centimetersToinches():
    centimeters = float(input("Enter value in Centimeters"))

    # conversion factor
    inches = centimeters * 0.3937

    print('%0.3f Centimeters is equal to %0.3f inches' % (centimeters, inches))


if __name__ == "__main__":
    print("Enter A Number (1-4) to Choose How to Convert:")
    print("1: Kilometres to Miles")
    print("2: Celsius to Fahrenheit")
    print("3: Degrees to Radians")
    print("4: Centimeters to Inches")

    user_input = int(input("Enter Here: "))
    if user_input == 1:
        kiloToMiles()
    elif user_input == 2:
        celsiusToFahrenheit()
    elif user_input == 3:
        degreesToradians()
    elif user_input == 4:
        centimetersToinches()
    else:
        print("Input is illegal !")

