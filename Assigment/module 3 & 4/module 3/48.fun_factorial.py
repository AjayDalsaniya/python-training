"""Write a Python function to calculate the factorial of a number (a 
nonnegative integer) """

#function
def fact_fun(num):
    fact = 1
    i=1
    while i <=num:
        fact=fact*i
        i=i+1
    print("Factorial Number : ",fact)
    
#user accept value
num1=int(input("Enter Number : "))
fact_fun(num1)