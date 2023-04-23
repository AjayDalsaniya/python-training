"""
Write a Python program that will return true if the two given integer
values are equal or their sum or difference is 5
    """


num1 = int(input("enter number 1:")) #10
num2 = int(input("enter number 2")) #20

if  abs(num1-num2) == 5 or num1+num2 ==5:
    print("Difference is 5")
else:
    print("No Difference is 5")