"""
How Do You Handle Exceptions With Try/Except/Finally In Python?
Explain with coding snippets. 


ans.
Try: This block will test the excepted error to occur
Except:  Here you can handle the error
Else: If there is no exception then this block will be executed
Finally: Finally block always gets executed either exception is generated or not

"""

def divide(x, y):
	try:
		result = x // y
	except ZeroDivisionError:
		print("Sorry ! You are dividing by zero ")
	else:
		print("Yeah ! Your answer is :", result)
	finally:
		print('This is always executed')

divide(3, 2)
