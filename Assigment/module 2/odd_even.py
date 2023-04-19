#odd and even number (prime)

num = int(input("Enter number"))
if num % 2 == 1:
    print("odd number",num)
else:
    print("even number",num)
    
start = int(input("Enter  number start  : "))
end = int(input("Enter  number end  : "))

for i in range(start, end + 1):
    if i % 2==0:
        print("even number : ",i)
        