"""
Write python program that swap two number with temp variable and
without temp variable.
"""

a = int(input("Enter a number 1:")) #10
b = int(input("enter a number 2:"))# 20

#temp variable
temp = a #10
a=b #20
b=temp #10

print("a : ",a) # 20
print("b : ",b) # 10

#without temp variable
c=10
d=20
c,d =d,c

print("without temp c ",c) #20
print("without temp d ",d) #10