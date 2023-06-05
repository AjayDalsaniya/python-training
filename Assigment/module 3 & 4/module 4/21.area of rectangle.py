"""Write a Python class named Rectangle constructed by a length and
width and a method which will compute the area of a rectangle 
"""


class rectangle1():
    def __init__(self,l,w):
        self.length = l 
        self.width = w
        
    def rec_area(self):
        return self.length * self.width

rect = rectangle1(3,4)
print(rect.rec_area())