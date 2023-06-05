"""Write a Python program to print all unique values in a dictionary"""
d={"1":"abc"}, {"2": "xyz"}, {"3": "abc"}, {"4": "asd"}, {"5":"asf"}, {"5":"azx"},{"6":"awe"}
a=[]# abc 
for i in d:
    for j in i.values():
        a.append(j)
print(set(a))