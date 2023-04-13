import math
class Goods(object):
    def getValue(self):
        return int(self.value)

    def getName(self):
        return str(self.name)

    def getNumber(self):
        return str(self.goodNum)

    def getQuan(self):
        return str(self.quan)

    def getCost(self):
        return self.cost

    def setQuan(self, newQuan):
        self.quan = int(newQuan)

    def __str__(self):
        return "\nItem Name: " + str(self.name) + "\nSingle Item Value: " + str(self.value) + \
               "\nGoods Number: " + str(self.goodNum)+"." + "\nGoods Quantity: " + str(self.quan) + "\n" + \
               "Total Item Value: " + str(self.quan * self.value) + "\n"

    def __init__(self, name, value, goodNum, cost, quan=1):
        self.name = name
        self.value = value
        self.goodNum = math.floor(goodNum)
        self.quan = quan
        self.cost = cost


class Customer(object):
    def addMallDollar(self, amount):
        self.mallDollar += amount

    def getName(self):
        return str(self.name)

    def getNumber(self):
        return str(self.customerNum)

    def getAddress(self):
        return str(self.address)

    def __str__(self):
        return "\nCustomer Name: " + str(self.name) + \
               "\nCustomer Address: " + str(self.address) + \
               "\nCustomer Number: " + str(self.customerNum) + \
               "\nMall Dollar: " + str(self.mallDollar) + "\n"

    def __init__(self, name, address, customerNum, mallDollar):
        self.name = name
        self.address = address
        self.customerNum = customerNum
        self.mallDollar = mallDollar


class Staff(object):
    def __str__(self):
        return "Staff Number: " + str(self.staffNum)

    def __init__(self, staffNum):
        self.staffNum = staffNum
