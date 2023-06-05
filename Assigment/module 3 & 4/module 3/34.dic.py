"""34.Write a Python script to check if a given key already exists in a
dictionary.
"""

dict1 = {1:20,2:50,3:100,4:500}

key = int(input("Enter key to check  in dictionary : "))
if  key in dict1:
    print("key already exist in dictionary")
else:
    print("key is not present in dictionary")
        
