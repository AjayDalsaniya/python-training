"""Write a Python program to read last n lines of a file"""

f =open("ajay.txt","r")
line = f.read().splitlines()
last_line = line[-1]

print(last_line)