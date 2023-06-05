"""
Write a Python program to find the repeated items of a tuple.
"""

tup = (1,2,3,4,3,5,2)
for i in tup: #1 2
    if tup.count(i)>1:
        print(i)#2 3