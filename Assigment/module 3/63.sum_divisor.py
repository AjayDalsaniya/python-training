"""Write a Python program to returns sum of all divisors of a number """
def sum_div(number):
    divisors = [1]
    for i in range(2, number):
        if (number % i)==0:
            divisors.append(i)
    print(divisors)
    return sum(divisors)
print("Sum " ,sum_div(12))
#print(sum_div(12))
