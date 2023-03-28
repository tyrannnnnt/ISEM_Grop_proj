from Order import *
from OrderNum import *
from others import *
import pandas as pd
import numpy as np


def readCustomer(fileName):
    customerFile = pd.read_excel(fileName)
    data = customerFile.values
    storeList = []
    for i in range(customerFile.shape[0]):
        # name, address, customerNum, mallDollar
        storeList.append(Customer(data[i][0], data[i][1], data[i][2], data[i][3]))
    return storeList


def readStaff(fileName):
    staffFile = pd.read_excel(fileName)
    data = staffFile.values
    storeList = []
    for i in range(staffFile.shape[0]):
        # staffNum
        storeList.append(Staff(data[i][0]))
    return storeList


def readOrderNum(fileName):
    orderFile = pd.read_excel(fileName)
    data = orderFile.values
    storeList = []
    lastOrderNum = data[0][0]
    for i in range(orderFile.shape[0]):
        # lastOrderNum, staffNum, modulusChar, itemNum
        newOrder = OrderNum(lastOrderNum, data[i][1], data[i][2], data[i][3])
        storeList.append(newOrder)
        lastOrderNum = newOrder.getWholeNum()
    return storeList


