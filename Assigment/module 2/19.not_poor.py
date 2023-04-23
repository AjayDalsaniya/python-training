""" Write a Python program to find the first appearance of the substring 
'not' and 'poor' from a given string, if 'not' follows the 'poor', replace the 
whole 'not'...'poor' substring with 'good'. Return the resulting string."""

str = "The lyrics is Not That Poor"
not1= str.find("Not")
poor = str.find("Poor")
print("not index : ",not1)
print("poor index : ",poor)

if(not1 < poor):
    print(str[:not1]+"Good")
    

