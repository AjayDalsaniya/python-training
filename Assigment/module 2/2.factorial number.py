"""Write a Python program to get the Factorial number of given number.
    """
n = int(input("Enter a number"))
fac =1
i=1
while i<=n:#check condition 1 2 3 4
    fac =fac*i # 1 2 6 24
    i=i+1
print("factiorial number",fac)
