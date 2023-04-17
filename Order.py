"""
Group A member:
CHENG MIN HSIU  19203144
ZHANG Jiayi     19250568
LIU Yulin       20250541
This file including the Class of order, it stores the information contained in the input order file. It contains some
functions calculating money amount, calculating digits and other specific functions.
"""

from datetime import datetime
import pandas as pd


class Order(object):
    """
    The Order Class storing the information of each order. Including functions of calculating money amount, check digits,
    judge statements and specific set and get functions.
    """
    def calSubTotal(self):
        """
        Calculate the subtotal price of the goods. Do the addition of each goods value * goods quantity.

        Returns:
            subtotal in float number with 2 decimal places
        """
        sum = 0.00
        for i in self.goodsList:
            sum += i.getValue() * int(i.getQuan())
        return round(sum, 2)

    def calDeliveryFee(self):
        """
        Calculate the delivery fee depending on the subTotal. If the subtotal bigger than 500, make it to zero. Else,
        make it 5% of the subtotal


        Returns:
            delivery fee in float number with 2 decimal places
        """
        if self.subTotal >= 500:
            return 0
        else:
            return round(0.05 * self.subTotal, 2)

    def calDiscount(self):
        """
        Calculate the discounts of VIP(0.5%) and VIP95(5%)

        Returns:
            discount in float number with 2 decimal places
        """
        return round(self.subTotal * 0.005, 2), round(self.subTotal * 0.05, 2)  # VIP(0.5%), VIP95(5%)

    def calTotal(self):
        """
        Calculate the total price. Subtotal - all the discounts

        Returns:
            total price
        """
        totalDis = self.VIPDis + self.VIP95Dis
        return self.subTotal - totalDis + self.calDeliveryFee()

    def calMallDollar(self):
        """
        Calculate the mall dollar depending on the total price

        Returns:
            mall dollar in floating number
        """
        if self.total >= 500:
            return round(self.total * 0.002)
        elif self.total >= 1000:
            return round(self.total * 0.0025)
        else:
            return 0

    def calHashTotal(self):
        """
        Add up the goods number as the hash total

        Returns:
            hash total
        """
        sum = 0
        for i in self.goodsList:
            sum = sum + int(i.getNumber())
        return sum

    def calNewHashTotal(self):
        """
        It uses the sum of item number and check digit as the NewHashTotal for the single order.

        Returns:
            new hash total in integer format
        """
        return int(self.orderNum.getItemNum()) + int(self.orderNum.getCheckDigit())

    def calProfit(self):
        """
        Calculate the profit made from the orders

        Returns:
            profit in floating number with 2 decimal places
        """
        cost = 0
        for i in self.goodsList:
            cost = cost + (int(i.getCost()) * int(i.getQuan()))
        # remove the delivery fee cost and vip discount
        cost = cost - self.deliveryFee - self.VIPDis - self.VIP95Dis
        return round(self.total - cost, 2)

    def calComplete(self):
        """
        Check if the order is completed according to the payment status and delivery status.
        The order will be completed if and only if its payCollection is Received and the delivered is T.

        Returns:
            1 or -1 as status
        """
        if self.delivered == "T" and self.paymentCollection == "Received":
            return 1
        else:
            return -1

    def getGoodsList(self):
        """
        Get the goods list

        Returns:
            goods list
        """
        strV = ""
        for i in range(len(self.goodsList)):
            strV = strV + str(self.goodsList[i])
        return strV

    def getOrderNumber(self):
        """
        Get and return the order number in String format

        Returns:
            order number in String format
        """
        return str(self.orderNum)

    def getOrderNumberF(self):
        """
        Get and return the order  in OrderNum Object format

        Returns:
            the order number object of this order
        """
        return self.orderNum

    def getTotal(self):
        """
        Get and return the total price

        Returns:
            total price of this order
        """
        return self.total

    def getComplete(self):
        """
        Get the complete status

        Returns:
            complete status of this order
        """
        return self.isComplete

    def getCompleteStr(self):
        """
        Convert and return the complete status in String format

        Returns:
            completion status in String format
        """
        if self.isComplete == -1:
            return "UnCompleted"
        else:
            return "Complete"

    def __str__(self):
        """The information contained in the orders: 
            order number, date, items, customer, subtotal, vip and vip95 discount, delivery fee, hash total, total amount
            Also includes profit, delivery status, payment status, order completion status as bonus.

            Bonus part:
            Profit: shows how much profit this order can make for the company
            Delivery status: shows the delivery status of the order
            Payment status: shows whether the payment is completed
            Completion status: If the order is paid and delivered, it is completed.

        Returns:
            The string of the information
        """
        return "InvoiceNum: " + str(self.orderNum) + "\n" + \
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
        """
        Initialize all the information in the order

        Args:
            orderNum (Object): order number
            orderDate (string): the date of the order
            goodsList (string list): the items in an order
            customer (Object): the customer
            paymentMethod (string): the payment method
            paymentCollection (string): whether the money transmission has finished
            delivered (string): whether the items are delivered
        """

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
