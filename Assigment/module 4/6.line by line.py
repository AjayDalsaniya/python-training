"""
    Write a Python program to read a file line by line and store it into a list
"""

f= open("ajay.txt","r") #read line by line 

print(f.read())


f.close()

f = open("ajay.txt","r") #display a text in list 
print(f.readlines())

f.close()