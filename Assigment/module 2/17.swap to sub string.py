"""Write a Python program to get a single string from two given strings, 
separated by a space and swap the first two characters of each string."""
a = "Tops "
b = "Technology"

a,b=b,a

#a = Terchnology
#b=Tops
print("a ",a[:2])
print("b ",b)
a1 = b[0:] + a[0:]


print(a1)