""" 
write a python program to sum of first n positive integers
"""

num = int(input("Enter number:"))

i = 1
sum =0
while i<=num:
    sum =sum +i
    i = i+1
print(sum)    