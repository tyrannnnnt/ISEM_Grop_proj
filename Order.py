import OrderNum
import others

# todo: ask VIP and VIPDay95 discount how much percent separately
class Order(object):
    def calSubTotal(self):
        sum = 0.00
        for i in self.orderList:
            sum += i.getValue()
        return round(sum, 2)

    def calDeliveryFee(self):
        if self.subTotal >= 500:
            return 0
        else:
            return round(0.05 * self.subTotal, 2)

    def calDiscount(self):
        # todo: how much percent
        return 0, 0

    def calTotal(self):
        totalDis = self.VIPDis + self.VIP95Dis
        return self.subTotal - totalDis + self.calDeliveryFee()

    def __init__(self, orderNum, orderDate, orderList, customer):
        self.orderNum = orderNum.getWholeNum()
        self.orderDate = orderDate
        self.orderList = orderList
        self.customer = customer
        self.subTotal = self.calSubTotal()
        self.VIPDis, self.VIP95Dis = self.calDiscount()
        self.deliveryFee = self.calDeliveryFee()
        self.total = self.calTotal()
