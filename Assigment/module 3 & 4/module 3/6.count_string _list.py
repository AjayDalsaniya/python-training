"""Write a Python program to count the number of strings where the string 
length is 2 or more and the first and last character are same from a given 
list of strings."""

li = ['aba', 'xyz',  '122','abc','xyzx']

x = 0
for i in li:
    if len(li) > 2 and i[0] == i[-1]:
        x=x+1#1
       
    
print("same word count",x)
    
            

