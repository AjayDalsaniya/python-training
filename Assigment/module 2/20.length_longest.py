"""Write a Python function that takes a list of words and returns the length 
of the longest one.
"""

a = ["hello","python programming","java"]
max1 =len(a)

#temp= a

for i in a:

    if (len(i)>max1):#hello 
        max1 = len(i) # 4 18
        temp = i # hello , python programming,
            
print("The word with the longest length is:", temp," and length is ", max1)