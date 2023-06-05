"""Write a Python function to check whether a number is in a given range"""
def givenrange(n):
    if n in range(1,6):
        print( " %s is in the range"%str(n))
    else :
        print("The number is outside the given range.")
givenrange(5)
