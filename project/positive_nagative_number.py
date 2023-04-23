""" accept two numbers and check entered number is positive or negative"""

positive_num = int(input("Enter number : "))
negative_num = int(input("Enter number : "))

if positive_num and negative_num  > 0:
    print("Number is Positive ")

elif positive_num and negative_num <0:
    print("Number is Nagative")
else:
    print("value is zero")
    
