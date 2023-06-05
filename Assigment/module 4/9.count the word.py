"""Write a Python program to count the number of lines in a text file. 
"""

f = open("ajay.txt","r")

word = len(f.readlines())

print(word)