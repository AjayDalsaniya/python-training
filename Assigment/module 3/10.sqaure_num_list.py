"""Write a Python program to generate and print a list of first and last 5
elements where the values are square of numbers between 1 and 30"""

list1 = [1,2,3,4,5,6]
s = []

for i in list1:
    square = i * i
    s.append(square)
    
print("List : ",list1)
print("Square ",s )



