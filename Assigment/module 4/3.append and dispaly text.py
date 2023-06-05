"""Write a Python program to append text to a file and display the text."""

f = open("ajay.txt","a") #create and append mode file

n= input("your name : ") #input name
f.write(n)  #store name in file
f.close()

f = open("ajay.txt","r")  #open file in read mode after display the text

print(f.read())

f.close()
