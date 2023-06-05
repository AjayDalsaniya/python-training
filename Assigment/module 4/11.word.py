"""Write a Python program to write a list to a file."""
   
# list of names
names = ['manthan', 'denish', 'ujas']

# open file in write mode
f=  open('ajay.txt', 'a') 
for item in names:
        # write each item on a new line
    f.write("%s\n" % item)
print('Done')