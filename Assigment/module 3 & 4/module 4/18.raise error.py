"""Write python program that user to enter only odd numbers, else will
raise an exception"""

try:
    num = int(input("Enter a number: "))
    assert num % 2 == 0
except:
    print("Not an even number!")
else:
    print("even")
    
