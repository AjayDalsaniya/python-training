"""
    Write a Python program to read a file line by line store it into a variable. 
"""
f = open("ajay.txt","r")

str = ""

for i in range(0,100):
    str = str + f.read(i) #store in variable to text
print(str)