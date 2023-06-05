"""4.Write a Python function to get the largest number, smallest num and sum 
of all from a list."""
#Function
def largest_number():
    list1 = [10,30,50,15,5,80]

    max1= max(list1)
    min1= min(list1)

    print("max : ",max1)
    print("min : ",min1)
    print("sum : ",sum(list1))

#function calling
largest_number()