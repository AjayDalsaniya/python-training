"""Write a Python program to count the occurrences of each word in a 
given sentence"""
cource_name  = "python java c++ c python c "

# Split the count into a list of words

words = cource_name.split()
print("\n",words) 


# Create an empty dictionary to store the word counts

word_counts = {}
# Iterate through the list of words

for i in words:#python=0 , java=1 c++ =2 c=3 python =4 
    if i  in  word_counts: 
        word_counts[i] += 1 # python 2
    else:
         word_counts[i] = 1 # python 1  java 1 c++ 1 c=1

print("\n",word_counts)

