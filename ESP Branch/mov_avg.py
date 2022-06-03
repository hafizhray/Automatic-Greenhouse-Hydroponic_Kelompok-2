class Mov_Avg():
    def __init__(self, n):
        self.val = [0] * n
        self.len = n
    
    def filter(self, val):
        self.val.pop(0)
        self.val.append(val)
        sum = 0
        for i in range(self.len):
            sum += self.val[i]
        return sum/self.len