import math


class Goods(object):
    """This is a new object class: goods
       It includes several get and set functions 

    Args:
        goods (object): items from the orders
    """
    def getValue(self):
        """Get the value of the item

        Returns:
            int: the value 
        """
        return int(self.value)

    def getName(self):
        """Get the name of the item

        Returns:
            string: item name
        """
        return str(self.name)

    def getNumber(self):
        """Get the item number

        Returns:
            string: item number
        """
        return str(self.goodNum)

    def getQuan(self):
        """Get the quantity of the item

        Returns:
            string: quantity
        """
        return str(self.quan)

    def getCost(self):
        """Get the cost of the item

        Returns:
            string: cost
        """
        return self.cost

    def setQuan(self, newQuan):
        """Set the quantity of the item

        Args:
            newQuan (int): quantity
        """
        self.quan = int(newQuan)

    def __str__(self):
        """The variables of items in correct format
        """
        
        return "\nItem Name: " + str(self.name) + "\nSingle Item Value: " + str(self.value) + \
               "\nGoods Number: " + str(self.goodNum)+"." + "\nGoods Quantity: " + str(self.quan) + "\n" + \
               "Total Item Value: " + str(self.quan * self.value) + "\n"

    def __init__(self, name, value, goodNum, cost, quan=1):
        """Initialize the item variables
        """
        self.name = name
        self.value = value
        self.goodNum = math.floor(goodNum)
        self.quan = quan
        self.cost = cost


class Customer(object):
    """This is a new object class: customer
       It includes several get and set functions 

    Args:
        Customer (object): customers
    """
    
    def addMallDollar(self, amount):
        """This function can add mall dollar to a customer

        Args:
            amount (int): the new mall dollar
        """
        self.mallDollar += amount

    def getName(self):
        """Get the name of the customer

        Returns:
            string: customer name
        """
        return str(self.name)

    def getNumber(self):
        """Get the customer number

        Returns:
            string: customer number
        """
        return str(self.customerNum)

    def getAddress(self):
        """Get the address of the customer

        Returns:
            string: address
        """
        return str(self.address)

    def __str__(self):
        """The customer information in correct order
        """
        return "\nCustomer Name: " + str(self.name) + \
               "\nCustomer Address: " + str(self.address) + \
               "\nCustomer Number: " + str(self.customerNum) + \
               "\nMall Dollar: " + str(self.mallDollar) + "\n"

    def __init__(self, name, address, customerNum, mallDollar):
        """Initialize the customer information

        Args:
            name (string): customer name
            address (string): customer address
            customerNum (string): customer number
            mallDollar (int): customer mall dollar
        """
        self.name = name
        self.address = address
        if len(str(customerNum)) != 6 or not str(customerNum).isdigit():
            print("Invalid input customer number format. Please Check!. " + customerNum)
            exit(1)
        self.customerNum = customerNum
        self.mallDollar = mallDollar


class Staff(object):
    """This is a new object class: staff
       It includes staff number

    Args:
        staff (object): staff number
    """
    def __str__(self):
        """The staff number
        """
        return "Staff Number: " + str(self.staffNum)

    def __init__(self, staffNum):
        """This function initialize the variable
        """
        self.staffNum = staffNum
