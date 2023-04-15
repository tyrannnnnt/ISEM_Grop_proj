# Please refer to "README.md" before running the program

from Order import *
from OrderNum import *
from others import *
import pandas as pd


def readCustomer(fileName):
    """Read in the customer names from excel"""
    customerFile = pd.read_excel(fileName)
    data = customerFile.values
    storeList = []
    for i in range(customerFile.shape[0]):
        # name, address, customerNum, mallDollar
        storeList.append(Customer(data[i][0], data[i][1], data[i][2], data[i][3]))
    return storeList


def readStaff(fileName):
    """Read in the staff names from excel"""
    staffFile = pd.read_excel(fileName)
    data = staffFile.values
    storeList = []
    for i in range(staffFile.shape[0]):
        # staffNum
        storeList.append(Staff(data[i][0]))
    return storeList


def readGoods(fileName):
    goodsFile = pd.read_excel(fileName)
    data = goodsFile.values
    totalGoodsList = []
    for i in range(goodsFile.shape[0]):
        # name, value, goodsNum, goodsCost
        totalGoodsList.append(Goods(data[i][0], data[i][1], data[i][2], data[i][3]))
    return totalGoodsList


def matchName(name, totalList):
    for i in range(len(totalList)):
        if totalList[i].getName() == name:
            return totalList[i]
    print("The query name do not exist, please check! : " + name)


def matchNumber(number, totalList):
    for i in range(len(totalList)):
        if str(totalList[i].getNumber()) == str(number):
            return totalList[i]
    print("The query number do not exist, please check!" + str(number))


def findCustomer(customerNumber, totalList):
    for i in range(len(totalList)):
        if str(totalList[i].getNumber()) == str(customerNumber):
            return totalList[i].getName(), totalList[i].getAddress()
    print("The customer number do not exist, please check!" + str(customerNumber))


def copyGood(good):
    return Goods(good.getName(), good.getValue(), int(good.getNumber()), int(good.getCost()))


def calNewHashTotal(storeList):
    total = 0
    for i in range(len(storeList)):
        total = total + storeList[i].calNewHashTotal()
    return total


def readOrder(fileName, totalGoodsList, customerList):
    orderFile = pd.read_excel(fileName)
    data = orderFile.values
    lastOrderNum = data[0][0]
    goodsList = []
    storeList = []
    count = 0
    for i in range(orderFile.shape[0]):
        items = data[i][2].replace(", ", ",").split(",")
        length = len(items)
        index = 0
        while length > 9:
            goodsList.append(items[(index * 9):((index + 1) * 9)])
            # lastOrderNum, staffNum, itemNum
            newOrder = OrderNum(lastOrderNum, data[i][1], 9)
            lastOrderNum = str(newOrder)
            orderGoods = []
            for j in goodsList[count]:
                identity = j.rsplit(" ", 1)[0]
                if identity.isdigit():
                    theGood = copyGood(matchNumber(identity, totalGoodsList))
                else:
                    theGood = copyGood(matchName(identity, totalGoodsList))
                theGood.setQuan(j.rsplit(" ", 1)[1])
                orderGoods.append(theGood)
            # orderNum, orderDate, goodsList, Customer, paymentMethod, paymentCollection, delivered
            storeList.append(Order(newOrder, data[i][3], orderGoods, matchNumber(data[i][4], customerList),
                                   data[i][5], data[i][6], data[i][7]))
            index = index + 1
            length = length - 9
            count = count + 1
        if length > 0:
            goodsList.append(items[(index * 9):])
            # lastOrderNum, staffNum, itemNum
            newOrder = OrderNum(lastOrderNum, data[i][1], len(goodsList[count]))
            lastOrderNum = str(newOrder)
            orderGoods = []
            for j in goodsList[count]:
                identity = j.rsplit(" ", 1)[0]
                if identity.isdigit():
                    theGood = copyGood(matchNumber(identity, totalGoodsList))
                else:
                    theGood = copyGood(matchName(identity, totalGoodsList))
                theGood.setQuan(j.rsplit(" ", 1)[1])
                orderGoods.append(theGood)
            # orderNum, orderDate, goodsList, Customer
            storeList.append(Order(newOrder, data[i][3], orderGoods, matchNumber(data[i][4], customerList),
                                   data[i][5], data[i][6], data[i][7]))
    return storeList


def printLastOrderFile(orderList, pathL="zzyTest/OutputLastOrderFile.txt"):
    file = open(pathL, "w")
    file.write(orderList[-1].getOrderNumber())
    file.close()


def printAuditedFile(orderList, pathA="zzyTest/OutputAuditedFile.txt"):
    file = open(pathA, "w")
    file.write("%-25s %d\n" % ("Number_of_orders", len(orderList)))
    file.write("%-25s %d\n" % ("Hash_total_of_orders", calNewHashTotal(orderList)))
    for i in range(len(orderList)):
        file.write("Order %d details\n" % i)
        file.write("---------------------\n")
        file.write("%-25s %s-%s\n" % ("Order_Number", orderList[i].getOrderNumberF().getAlphabet(),
                                      str(orderList[i].getOrderNumberF().getSeqNum())))
        file.write("%-25s %s\n" % ("Agency_number", str(orderList[i].getOrderNumberF().getStaffNum())))
        file.write("%-25s %s\n" % ("Modulus_number", str(orderList[i].getOrderNumberF().getModulusNum())))
        file.write("%-25s %s\n" % ("Total", str(orderList[i].getTotal())))
        file.write("%-25s %s\n\n" % ("Hash_total", str(orderList[i].calHashTotal())))
    file.close()


def printAllOrder(orderList):
    for i in orderList:
        print("-------------------------------------------------------------------------\n")
        print(i)


def printAllUnComplete(orderList):
    for i in orderList:
        if str(i.getComplete()) == "-1":
            print("-------------------------------------------------------------------------\n")
            print(i)


def searchOrder(orderNum, orderList):
    for i in orderList:
        if str(i.getOrderNumber()) == orderNum:
            print(i)
            return
    print("The Order Number " + orderNum + " is not found")


try:
    theCustomerList = readCustomer("zzyTest/Customer.xlsx")
    theStaffList = readStaff("zzyTest/Staff.xlsx")
    theGoodsList = readGoods("zzyTest/Goods.xlsx")
    theOrderList = readOrder("zzyTest/Order.xlsx", theGoodsList, theCustomerList)
except IOError:
    print(IOError)
    exit(1)
except ValueError:
    print(ValueError)
    exit(1)
except Exception:
    print(Exception)
    exit(1)

isExit = False
while not isExit:
    instruction = input("Please input the instruction: \n"
                        "1. Output last order file\n"
                        "2. Output audited file\n"
                        "3. Output detail of All orders\n"
                        "4. Output detail information of specific order Number\n"
                        "5. Print all Uncompleted Order(In Transit and not delivered)\n"
                        "6. Load another Customer file(It will cover the original one!)\n"
                        "7. Load another Staff file(It will cover the original one!)\n"
                        "8. Load another Order file(It will cover the original one!)\n"
                        "9. Exit\n")

    if instruction == "1":
        path = input("Please input the expect path, "
                     "if you input -1, the path will be default: zzyTest/OutputLastOrderFile.txt\n")
        try:
            if path != "-1":
                printLastOrderFile(theOrderList, path)
            else:
                printLastOrderFile(theOrderList)
            print("The Last Order file has been output!\n")
        except IOError:
            print(IOError)
        except ValueError:
            print(ValueError)
        except Exception:
            print(Exception)

    elif instruction == "2":
        path = input("Please input the expect path, "
                     "if you input -1, the path will be default: zzyTest/OutputAuditedFile.txt\n")
        try:
            if path != "-1":
                printAuditedFile(theOrderList, path)
            else:
                printAuditedFile(theOrderList)
            print("The audited file has been output!\n")
        except IOError:
            print(IOError)
        except ValueError:
            print(ValueError)
        except Exception:
            print(Exception)

    elif instruction == "3":
        printAllOrder(theOrderList)

    elif instruction == "4":
        findOrder = input("Please input the order number you want to search(please include the () of the digit): \n")
        try:
            searchOrder(findOrder, theOrderList)
        except ValueError:
            print(ValueError)
        except Exception:
            print(Exception)

    elif instruction == "5":
        printAllUnComplete(theOrderList)

    elif instruction == "6":
        path = input("Please input the expect path, "
                     "if you input -1, the path will be default: zzyTest/Customer.xlsx\n")
        if path == "-1":
            path = "zzyTest/Customer.xlsx"
        try:
            theCustomerList = readCustomer(path)
        except IOError:
            print(IOError)
        except ValueError:
            print(ValueError)
        except Exception:
            print(Exception)

    elif instruction == "7":
        path = input("Please input the expect path, "
                     "if you input -1, the path will be default: zzyTest/Staff.xlsx\n")
        if path == "-1":
            path = "zzyTest/Staff.xlsx"
        try:
            theStaffList = readStaff(path)
        except IOError:
            print(IOError)
        except ValueError:
            print(ValueError)
        except Exception:
            print(Exception)

    elif instruction == "8":
        path = input("Please input the expect path, "
                     "if you input -1, the path will be default: zzyTest/Order.xlsx\n")
        if path == "-1":
            path = "zzyTest/Order.xlsx"
        try:
            theOrderList = readOrder(path, theGoodsList, theCustomerList)
        except IOError:
            print(IOError)
        except ValueError:
            print(ValueError)
        except Exception:
            print(Exception)

    elif instruction == "9":
        isExit = True
    else:
        print("Invalid input instruction number, please check!")
