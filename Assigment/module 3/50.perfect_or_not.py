"""Write a Python function to check whether a number is perfect or not. """

def perNot():
    n = int(input("Enter any number: "))#6
    sum1 = 0
    for i in range(1, n):#1 2 3 4
        if(n % i == 0):
            sum1 = sum1 + i#1 3 6
    if (sum1 == n):
        print("The number is a Perfect number!")
    else:
        print("The number is not a Perfect number!")
perNot()