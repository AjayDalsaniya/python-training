"""Write a python program to find the longest words"""
f= open("ajay.txt","r")

wordslist = f.read().split()
print("wordslist : ",wordslist)

# Storing all the words having the maximum length(longest word length)
longestword = len(max(wordslist, key=len))
print("longestword : ",longestword)

# Here, we are checking all the words whose length is equal to that of the longest word
for t in wordslist:
    if len(t)==longestword:
        # Print the longest words from a text file
        print(t)