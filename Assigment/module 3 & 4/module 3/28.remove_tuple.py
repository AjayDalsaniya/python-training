""""Write a Python program to remove an empty tuple(s) from a list of tuples."""
list1 = [(1,2,3),(4,5),()]

for tuple in list1:
    print(tuple)
    if (len(tuple)==0):
        list1.remove(tuple)
        
print(list1)
