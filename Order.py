from OrderNum import *
from others import *
from datetime import datetime
import pandas as pd

# A new class order
class Order(object):
    def calSubTotal(self):
        '''Calculate the total price of the goods'''
        sum = 0.00
        for i in self.goodsList:
            sum += i.getValue() * int(i.getQuan())
        return round(sum, 2)

    def calDeliveryFee(self):
        '''Calculate the delivery fee depending on the subTotal'''
        if self.subTotal >= 500:
            return 0
        else:
            return round(0.05 * self.subTotal, 2)

    def calDiscount(self):
        '''Calculate the discount'''
        return round(self.subTotal * 0.005, 2), round(self.subTotal * 0.05, 2)  # VIP(0.5%), VIP95(5%)

    def calTotal(self):
        '''Calculate the total price. Subtotal - all the discounts'''
        totalDis = self.VIPDis + self.VIP95Dis
        return self.subTotal - totalDis + self.calDeliveryFee()

    def calMallDollar(self):
        '''Calculate the mall dollar depending on the total price'''
        if self.total >= 500:
            return round(self.total * 0.002)
        elif self.total >= 1000:
            return round(self.total * 0.0025)
        else:
            return 0

    def calHashTotal(self):
        '''Add the item number as the hash total'''
        sum = 0
        for i in self.goodsList:
            sum = sum + int(i.getNumber())
        return sum

    def calNewHashTotal(self):
        '''We use the sum of item number and check digit here'''
        return int(self.orderNum.getItemNum()) + int(self.orderNum.getCheckDigit())

    def calProfit(self):
        '''Calculate the profit made from the orders'''
        cost = 0
        for i in self.goodsList:
            cost = cost + (int(i.getCost()) * int(i.getQuan()))
        return round(self.total - cost, 2)

    def calComplete(self):
        '''Check if the order is completed according to the payment status and delivery status'''
        if self.delivered == "T" and self.paymentCollection == "Received":
            return 1
        else:
            return -1

    def getGoodsList(self):
        '''Get the item list'''
        strV = ""
        for i in range(len(self.goodsList)):
            strV = strV + str(self.goodsList[i])
        return strV

    def getOrderNumber(self):
        '''Get and return the order number in String format'''
        return str(self.orderNum)

    def getOrderNumberF(self):
        '''Get and return the order number'''
        return self.orderNum

    def getTotal(self):
        '''Get and return the total price'''
        return self.total

    def getComplete(self):
        '''Get the complete status'''
        return self.isComplete

    def getCompleteStr(self):
        '''Return the complete status'''
        if self.isComplete == -1:
            return "UnComplete"
        else:
            return "returnComplete"

    def __str__(self):
        '''The information contained in the orders: 
            order number, date, items, customer, subtotal, vip and vip95 discount, delivery fee, hash total, total amount
            Also includes profit, delivery status, payment status, roder completion status as bonus'''
        return "OrderNum: " + str(self.orderNum) + "\n" + \
               "OrderDate: " + str(self.orderDate) + "\n" + \
               "Goods: " + str(self.getGoodsList()) + "\n" + \
               "Customer: " + str(self.customer) + "\n" + \
               "SubTotal: " + str(self.subTotal) + "\n" + \
               "VIPDiscount: " + str(self.VIPDis) + "\n" + \
               "VIP95Dis: " + str(self.VIP95Dis) + "\n" + \
               "DeliveryFee: " + str(self.deliveryFee) + "\n" + \
               "TotalAmount: " + str(self.total) + "\n" + \
               "Hash Total: " + str(self.calHashTotal()) + "\n" + \
               "The order profit: " + str(self.profit) + "\n" + \
               "The payment method: " + str(self.paymentMethod) + "\n" + \
               "The payment collection: " + str(self.paymentCollection) + "\n" + \
               "Delivered or not: " + str(self.delivered) + "\n" + \
               "Complete or not: " + str(self.getCompleteStr()) + "\n" + \
               "-------------------------------------------------------------------------\n"

    def __init__(self, orderNum, orderDate, goodsList, customer, paymentMethod, paymentCollection, delivered):
        '''Initialize all the information in the order'''
        self.orderNum = orderNum
        date = pd.to_datetime(orderDate)
        self.orderDate = datetime.date(date)
        self.goodsList = goodsList
        self.customer = customer
        self.subTotal = self.calSubTotal()
        self.VIPDis, self.VIP95Dis = self.calDiscount()
        self.deliveryFee = self.calDeliveryFee()
        self.total = self.calTotal()
        self.customer.addMallDollar(self.calMallDollar())
        self.profit = self.calProfit()
        self.paymentMethod = paymentMethod
        self.paymentCollection = paymentCollection
        self.delivered = delivered
        self.isComplete = self.calComplete()
