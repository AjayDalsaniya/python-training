""" Write a Python program to get the Fibonacci series of given range.
"""

num1 = int(input("Enter Number "))

x= 0
y=1
z=0

while z<=num1:
     print(z)# 0 1 1 2 3 5
     x= y # 1 0 1 1 2
     y=z # 0 1 1 2 3
     z=x+y# 1 1 2 3 5
     