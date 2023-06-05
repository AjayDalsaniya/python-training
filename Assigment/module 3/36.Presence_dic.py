"""How Do You Check The Presence Of A Key In A Dictionary?"""

dict1 = {1:"akhil",2:"nikhil",3:"abc",4:"xyz"}
x= int(input("please enter key number : "))
if x in dict1.keys():
    print("true")
else:
    print("false")