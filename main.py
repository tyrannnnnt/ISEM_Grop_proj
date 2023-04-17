# Please refer to "README.md" before running the program

from Order import *
from OrderNum import *
from others import *
import pandas as pd
import traceback


def readCustomer(fileName):
    """Read in the customer names from excel
    
    Args:
        fileName(string): the file to read

    Returns:
        list: customers
    """
    customerFile = pd.read_excel(fileName, engine='openpyxl')
    data = customerFile.values
    storeList = []
    for i in range(customerFile.shape[0]):
        # name, address, customerNum, mallDollar
        storeList.append(Customer(data[i][0], data[i][1], data[i][2], data[i][3]))
    return storeList


def readStaff(fileName):
    """Read in the staff names from excel
    
    Args:
        fileName(string): the file to read

    Returns:
        list: staffs
    """
    staffFile = pd.read_excel(fileName, engine='openpyxl')
    data = staffFile.values
    storeList = []
    for i in range(staffFile.shape[0]):
        # staffNum
        storeList.append(Staff(data[i][0]))
    return storeList


def readGoods(fileName):
    """Read in the item list
    
    Args:
        fileName(string): the file to read

    Returns:
        list: items
    """
    goodsFile = pd.read_excel(fileName, engine='openpyxl')
    data = goodsFile.values
    totalGoodsList = []
    for i in range(goodsFile.shape[0]):
        # name, value, goodsNum, goodsCost
        totalGoodsList.append(Goods(data[i][0], data[i][1], data[i][2], data[i][3]))
    return totalGoodsList


def matchName(name, totalList):
    """ Check if the name can match with the list

    Args:
        name (string): the name to search
        totalList (list): the total list

    Returns:
        element in list: the matched information
        error message: if not matched    
    """
    for i in range(len(totalList)):
        if totalList[i].getName() == name:
            return totalList[i]
    print("The query name do not exist, please check! : " + name)


def matchNumber(number, totalList):
    """Check if the number can match with the list

    Args:
        number (int): the number to search
        totalList (list): the total list

    Returns:
        element in list: the matched information
        error message: if not matched
    """
    for i in range(len(totalList)):
        if str(totalList[i].getNumber()) == str(number):
            return totalList[i]
    print("The query number do not exist, please check!" + str(number))


def findCustomer(customerNumber, totalList):
    """This function can be used to look for a customer
    
    Args:
        customerNumber: the customer to search
        totalList: the total list

    Returns:
        element in list: name and address
        error message: if not found
    """
    for i in range(len(totalList)):
        if str(totalList[i].getNumber()) == str(customerNumber):
            return totalList[i].getName(), totalList[i].getAddress()
    print("The customer number do not exist, please check!" + str(customerNumber))


def copyGood(good):
    """This function can be used to copy goods
       If the items are copied directly, they may be stored at the same address in the computer although showed in two lists. 
       When one is changed, the other one may also be changed. This copy function is to create another storage space for the 
       copied items so that the quantity will not be interferred.

    Args:
        good (good): item to be copied

    Returns:
        good: the copied good
    """
    return Goods(good.getName(), good.getValue(), int(good.getNumber()), int(good.getCost()))


def calNewHashTotal(storeList):
    """Calculate the new hash total

    Args:
        storeList (list): the list

    Returns:
        float: total price
    """
    total = 0
    for i in range(len(storeList)):
        total = total + storeList[i].calNewHashTotal()
    return total


def readOrder(fileName, totalGoodsList, customerList):
    """Read in the order information

    Args:
        fileName (file): file to read
        totalGoodsList (list): the item list
        customerList (list): the customer name list

    Returns:
        _type_: _description_
    """
    orderFile = pd.read_excel(fileName, engine='openpyxl')
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
                    try:
                        theGood.setQuan(j.rsplit(" ", 1)[1])
                    except IndexError:
                        print(IndexError)
                        print(" Please make sure your input file format is correct.")
                        exit(1)
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
            try:
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
            except ValueError:
                print(ValueError)
                print("Please check your data in last order number, staff number and item number. It cannot be empty or in wrong format")
                exit(1)
            except IndexError:
                print(IndexError)
                print("Please check your staff number or customer number. It cannot be empty or in wrong format")
                exit(1)
            # orderNum, orderDate, goodsList, Customer
            storeList.append(Order(newOrder, data[i][3], orderGoods, matchNumber(data[i][4], customerList),
                                   data[i][5], data[i][6], data[i][7]))
            count = count + 1
    return storeList


def printLastOrderFile(orderList, pathL="zzyTest/OutputLastOrderFile.txt"):
    """Print the last order into a file

    Args:
        orderList (list): the orders
        pathL (str): the path to print. Defaults to "zzyTest/OutputLastOrderFile.txt".
    """
    file = open(pathL, "w")
    file.write(orderList[-1].getOrderNumber())
    file.close()


def printAuditedFile(orderList, pathA="zzyTest/OutputAuditedFile.txt"):
    """This is the print function Will first set a new path and print out into a txt document

    Args:
        orderList (list): the orders
        pathA (str): the path to print. Defaults to "zzyTest/OutputAuditedFile.txt".
    """
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
    """This prints out all the orders with a loop

    Args:
        orderList (list): the orders
    """
    for i in orderList:
        print("-------------------------------------------------------------------------\n")
        print(i)


def printAllUnComplete(orderList):
    """This prints out all the uncomplete orders

    Args:
        orderList (list): the orders
    """
    for i in orderList:
        if str(i.getComplete()) == "-1":
            print("-------------------------------------------------------------------------\n")
            print(i)


def searchOrder(orderNum, orderList):
    """This can be used to search for an order.
       If found, print out. If not, return error message.

    Args:
        orderNum (int): the order to search
        orderList (list): the orders
    """
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
    traceback.print_exc()
    exit(1)
except ValueError:
    print(ValueError)
    traceback.print_exc()
    exit(1)



    """Read user input to select the operations
    """
isExit = False
while not isExit:
    instruction = input("Please input the instruction: \n"
                        "1. Output last order file\n"
                        "2. Output audited file\n"
                        "3. Output detail of All orders\n"
                        "4. Output detail information of specific Invoice Number\n"
                        "5. Print all Uncompleted Order(In Transit and not delivered)\n"
                        "6. Load another Customer file(It will cover the original one!)\n"
                        "7. Load another Staff file(It will cover the original one!)\n"
                        "8. Load another Order file(It will cover the original one!)\n"
                        "9. Load another Goods file(It will cover the original one!)\n"
                        "10. Exit\n")

    if instruction == "1":
        """Call print last order function
        """
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
            traceback.print_exc()
            print("\n")
            continue
        except ValueError:
            print(ValueError)
            traceback.print_exc()
            print("\n")
            continue

    elif instruction == "2":
        """Call print audited file function
        """
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
            traceback.print_exc()
            print("\n")
            continue
        except ValueError:
            print(ValueError)
            traceback.print_exc()
            print("\n")
            continue

    elif instruction == "3":
        """Call print all order function
        """
        printAllOrder(theOrderList)
    elif instruction == "4":
        """Search the order and print out the information of the order
        """
        findOrder = input("Please input the order number you want to search(please include the () of the digit): \n")
        try:
            searchOrder(findOrder, theOrderList)
        except ValueError:
            print(ValueError)
            traceback.print_exc()
            print("\n")
            continue

    elif instruction == "5":
        """Print all Uncompleted Order
        """
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
            traceback.print_exc()
            print("\n")
            continue
        except ValueError:
            print(ValueError)
            traceback.print_exc()
            print("\n")
            continue

    elif instruction == "7":
        path = input("Please input the expect path, "
                     "if you input -1, the path will be default: zzyTest/Staff.xlsx\n")
        if path == "-1":
            path = "zzyTest/Staff.xlsx"
        try:
            theStaffList = readStaff(path)
        except IOError:
            print(IOError)
            traceback.print_exc()
            print("\n")
            continue
        except ValueError:
            print(ValueError)
            traceback.print_exc()
            print("\n")
            continue

    elif instruction == "8":
        path = input("Please input the expect path, "
                     "if you input -1, the path will be default: zzyTest/Order.xlsx\n")
        if path == "-1":
            path = "zzyTest/Order.xlsx"
        try:
            theOrderList = readOrder(path, theGoodsList, theCustomerList)
        except IOError:
            print(IOError)
            traceback.print_exc()
            print("\n")
            continue
        except ValueError:
            print(ValueError)
            traceback.print_exc()
            print("\n")
            continue

    elif instruction == "9":
        path = input("Please input the expect path, "
                     "if you input -1, the path will be default: zzyTest/Goods.xlsx\n")
        if path == "-1":
            path = "zzyTest/Goods.xlsx"
        try:
            theGoodsList = readGoods(path)
        except IOError:
            print(IOError.args)
            traceback.print_exc()
            print("\n")
            continue
        except ValueError:
            print(ValueError)
            traceback.print_exc()
            print("\n")
            continue

    elif instruction == "10":
        isExit = True
    else:
        print("Invalid input instruction number, please check!")
