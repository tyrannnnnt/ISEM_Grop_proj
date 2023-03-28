from OrderNum import *
from others import *


# todo: ask VIP and VIPDay95 discount how much percent separately
class Order(object):
    def calSubTotal(self):
        sum = 0.00
        for i in self.goodsList:
            sum += i.getValue()
        return round(sum, 2)

    def calDeliveryFee(self):
        if self.subTotal >= 500:
            return 0
        else:
            return round(0.05 * self.subTotal, 2)

    def calDiscount(self):
        # todo: how much percent
        return 2, round(self.subTotal*0.95, 2)   # VIP, VIP95

    def calTotal(self):
        totalDis = self.VIPDis + self.VIP95Dis
        return self.subTotal - totalDis + self.calDeliveryFee()

    def calMallDollar(self):
        if self.total >= 500:
            return round(self.total * 0.002)
        elif self.total >= 1000:
            return round(self.total * 0.0025)
        else:
            return 0

    def calHashTotal(self):
        sum = 0
        for i in self.goodsList:
            sum += i.getGoodNum()
        return sum

    def __init__(self, orderNum, orderDate, goodsList, customer):
        self.orderNum = orderNum.getWholeNum()
        self.orderDate = orderDate
        self.goodsList = goodsList
        self.customer = customer
        self.subTotal = self.calSubTotal()
        self.VIPDis, self.VIP95Dis = self.calDiscount()
        self.deliveryFee = self.calDeliveryFee()
        self.total = self.calTotal()
