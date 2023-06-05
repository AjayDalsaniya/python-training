"""Write a Python program to get unique values from a list"""
ul=[1,2,4,5,6,5]
nl = []
for i in ul:
    if i not in nl:
        nl.append(i) 
print(nl)