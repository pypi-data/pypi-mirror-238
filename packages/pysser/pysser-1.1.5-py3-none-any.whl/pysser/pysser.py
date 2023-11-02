  
def add(a, b):  
    """加法函数，返回两个数的和"""  
    return a + b  
  
def multiply(a, b):  
    """乘法函数，返回两个数的积"""  
    return a * b


class Area():
    def __init__(self):
        self.area = 0
        self.area_max = 0
        self.area_min = 0
        self.area_avg = 0
        self.area_sum = 0
        self.area_count = 0

    def setMax(self, max):
        self.area_max = max
    def getMax(self):
        return self.area_max