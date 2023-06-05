"""Write a Python program to create and display all combinations of letters,
selecting each letter from a different key in a dictionary."""

dic =  {'1': ['a','b'], '2': ['c','d']}

dic1 = dic['1']
dic2 = dic['2']

for i in dic1:
    for j in dic2:
        print(i+j)#ac
    