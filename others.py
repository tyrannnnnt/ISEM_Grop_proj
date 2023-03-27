class Goods(object):
    def getValue(self):
        return self.value

    def getName(self):
        return self.name

    def getGoodNum(self):
        return self.goodNum

    def __init__(self, name, value, goodNum):
        self.name = name
        self.value = value
        self.goodNum = goodNum


class Customer(object):
    def __init__(self, name, address, customerNum):
        self.name = name
        self.address = address
        self.customerNum = customerNum
