"""What is File function in python? 
    -> Python file object provides methods and attributes to access and manipulate files. 
        Using file objects, we can read or write any files

What is keywords to create and write file. 
    -> write()

"""

f = open("ajay.txt","w") #create a new file with write mode .

n = input("Enter your name : ")  
f.write(n)  #we can store data in file
f.close()