class Goods(object):
    def getValue(self):
        return int(self.value)

    def getName(self):
        return str(self.name)

    def getGoodNum(self):
        return str(self.goodNum)

    def __str__(self):
        return "Item Name: " + str(self.name) + "\nItem Value: " + str(self.value) +\
                "\nGoods Number: " + str(self.goodNum)

    def __init__(self, name, value, goodNum):
        self.name = name
        self.value = value
        self.goodNum = goodNum


class Customer(object):
    def addMallDollar(self, amount):
        self.mallDollar += amount

    def __str__(self):
        return "Customer Name: " + str(self.name) +\
               "\nCustomer Address: " + str(self.address) +\
               "\nCustomer Number: " + str(self.customerNum) +\
               "\nMall Dollar: " + str(self.mallDollar)

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
