"""Write a Python program to sum of three given integers. However, if 
two values are equal sum will be zero.
"""

num1 = int(input("Enter number 1 : "))#10
num2 = int(input("Enter number 2 : "))#10
num3 = int(input("Enter number 3 : "))#20

if num1 == num2 or num1 == num3 or num2 == num3 :
    print("Zero")
else:
    sum = num1+num2+num3
    print("Sum : ",sum) 