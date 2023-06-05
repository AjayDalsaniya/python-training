"""Write a Python program to check whether a list contains a sub list """

list1 = [1,5,6,10,11,13,15]
list2=[5,7,10]

for i in list1:#1 5  6 10 
    for j in list2:#5
        if i==j:
            print(i)#5 10