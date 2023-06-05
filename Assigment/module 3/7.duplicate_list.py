"""Write a Python program to remove duplicates from a list."""

list = [10, 20, 30, 20, 10, 50, 60, 40, 80, 50, 40]
print(list)

for x in list:#10, 20 30  20  10 50 60 40 80 50 40
    if list.count(x) > 1:
        list.remove(x)#10 20 50 40
        
print(list) #30 20 10 60 80 50 40
    

