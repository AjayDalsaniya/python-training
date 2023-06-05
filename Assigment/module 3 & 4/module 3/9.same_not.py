"""Write a Python function that takes two lists and returns true if they have
at least one common member(same Number)."""

def myfun():
    list1 = [10,20,30,40,50]
    list2 = [40,60,70,80,90,100]


    for i in list1:#10 20 
        for j in list2:#40 60
            if j==i:
                return True
            else:
                return False
print(myfun())
    