# Calculate the area of a Triangle, rectangle, circle, trapezoid.


import math


def triangle():

    a = float(input('Enter first side: '))
    b = float(input('Enter second side: '))
    c = float(input('Enter third side: '))

    s = (a + b + c) / 2

    area = (s * (s - a) * (s - b) * (s - c)) ** 0.5
    print('The area of the triangle is %0.2f' % area)


def rectangle():

    a = float(input('Enter length of side A: '))
    b = float(input('Enter length of side B: '))

    area = a*b

    print('The area of the rectangle is %0.3f' % area)


def circle():
    r = float(input('Enter radius of the circle: '))

    # conversion factor
    area = math.pi * r * r

    print('The area of the circle is %0.3f' % area)


def trapezoids():
    base1 = float(input('Enter the First Base of a Trapezoid: '))
    base2 = float(input('Enter the Second Base of a Trapezoid: '))
    height = float(input('Enter the Height of a Trapezoid: '))

    Area = 0.5 * (base1 + base2) * height

    print("Area of a Trapezium = %.3f " % Area)


if __name__ == "__main__":
    print("Enter A Number (1-4) to Choose How to Convert:")
    print("1: Area of triangle")
    print("2: Area of rectangle")
    print("3: Area of circle")
    print("4: Area of trapezoids")

    user_input = int(input("Enter Here: "))
    if user_input == 1:
        triangle()
    elif user_input == 2:
        rectangle()
    elif user_input == 3:
        circle()
    elif user_input == 4:
        trapezoids()
    else:
        print("Input is illegal !")

