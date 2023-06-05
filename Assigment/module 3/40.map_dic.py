"""Write a Python program to map two lists into a dictionary"""
Product = ["mobile","tv","laptop"]#key

qty = [100,50,25]#value

dict1 = dict(zip(Product,qty))
print(dict1)