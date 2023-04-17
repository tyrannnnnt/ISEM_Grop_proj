"""
Group A member:
CHENG MIN HSIU  19203144
ZHANG Jiayi     19250568
LIU Yulin       20250541
This project aims to provide the Flexible Hashing and Checking Digit creation function and is able to verify the
validity of the Invoice produced by the online ordering systems. The deatial information of the order are also provided.
Please make sure your environment exist "openpyxl" model for handling the Excel(.xlsx) file. You can read the
"README.md" file for the instruction of the inputting file format and the details of the output and the functions of
the project.
"""

from Order import *
from OrderNum import *
from others import *
import pandas as pd
import traceback


def readCustomer(fileName):
    """Read in the customer information from the input path (Excel file)
    
    Args:
        fileName(string): the file path to read

    Returns:
        list: list of Customer, storing customers' information with structured data
    """
    # read the Excel file
    customerFile = pd.read_excel(fileName, engine='openpyxl')
    # get values
    data = customerFile.values
    storeList = []
    for i in range(customerFile.shape[0]):
        # name, address, customerNum, mallDollar
        storeList.append(Customer(data[i][0], data[i][1], data[i][2], data[i][3]))
    return storeList


def readStaff(fileName):
    """Read in the staff information from the input path (Excel file)
    
    Args:
        fileName(string): the file path to read

    Returns:
        list: list of Staff, storing staffs' information with structured data
    """
    # read the Excel file
    staffFile = pd.read_excel(fileName, engine='openpyxl')
    # get values
    data = staffFile.values
    storeList = []
    for i in range(staffFile.shape[0]):
        # staffNum
        storeList.append(Staff(data[i][0]))
    return storeList


def readGoods(fileName):
    """Read in the goods information from the input path (Excel file)

    Args:
        fileName(string): the file path to read

    Returns:
        list: list of Goods, storing goods' information with structured data
    """
    # read Excel file
    goodsFile = pd.read_excel(fileName, engine='openpyxl')
    # get values from the file
    data = goodsFile.values
    totalGoodsList = []
    for i in range(goodsFile.shape[0]):
        # name, value, goodsNum, goodsCost
        totalGoodsList.append(Goods(data[i][0], data[i][1], data[i][2], data[i][3]))
    return totalGoodsList


def matchName(name, totalList):
    """ Find and return the object in the totalList with the same name with the input name

    Args:
        name (string): the name to search
        totalList (list): the total list containing the name

    Returns:
        element in list: the object matched information with the input name
        error message: if it cannot find the corresponding object, print the error message
    """
    for i in range(len(totalList)):
        if totalList[i].getName() == name:
            return totalList[i]
    print("The query name do not exist, please check! : " + name)


def matchNumber(number, totalList):
    """ Find and return the object in the totalList with the same number with the input name

        Args:
            number (string): the number to search
            totalList (list): the total list containing the number

        Returns:
            element in list: the object matched information with the input number
            error message: if it cannot find the corresponding object, print the error message
        """
    for i in range(len(totalList)):
        if str(totalList[i].getNumber()) == str(number):
            return totalList[i]
    print("The query number do not exist, please check!" + str(number))


def findCustomer(customerNumber, totalList):
    """This function can be used to look for a customer according to the input customer number in the totalList of the
    customer.
    
    Args:
        customerNumber: the customer number need to search
        totalList: the total list storing the customer

    Returns:
        object information: name and address of the found object
        error message: if it not found the customer in the totalList has the same customer number
    """
    for i in range(len(totalList)):
        if str(totalList[i].getNumber()) == str(customerNumber):
            return totalList[i].getName(), totalList[i].getAddress()
    print("The customer number do not exist, please check!" + str(customerNumber))


def copyGoods(goods):
    """This function can be used to do the deep copy of Goods Object
       If the items are copied directly, they may be stored at the same address in the computer although showed in two lists. 
       When one is changed, the other one may also be changed. This copy function is to create another storage space for the 
       copied items so that the quantity will not be interfered.

    Args:
        goods (goods): item need to be deep copied

    Returns:
        goods: the copied goods
    """
    return Goods(goods.getName(), goods.getValue(), int(goods.getNumber()), int(goods.getCost()))


def calNewHashTotal(storeList):
    """Calculate the new hash total by adding each of the NewHashTotal in the order object.

    Args:
        storeList (list): the list store the orders

    Returns:
        int: new hash total of the order list
    """
    total = 0
    for i in range(len(storeList)):
        total = total + storeList[i].calNewHashTotal()
    return total


def readOrder(fileName, totalGoodsList, customerList):
    """Read in the order information from the input path (Excel file)

    Args:
        fileName(string): the file path to read
        totalGoodsList(list): all goods list
        customerList(list): all customer list

    Returns:
        list: list of Order object, storing the information of the order
    """
    # read file from the Excel
    orderFile = pd.read_excel(fileName, engine='openpyxl')
    # get values from the file
    data = orderFile.values
    # get the last order number from the first order
    lastOrderNum = data[0][0]
    # input goods List
    goodsList = []
    # the List store the generated order number
    storeList = []
    # the count for actual order number
    count = 0
    # for each row
    for i in range(orderFile.shape[0]):
        items = data[i][2].replace(", ", ",").split(",")
        length = len(items)
        index = 0
        if data[i][5] != 'Credit Card' and data[i][5] != 'FPS' and data[i][5] != 'E Wallet' and data[i][5] != 'Mobile':
            print("Caution! Please input valid payment method")
            exit()
        if data[i][6] != 'In Transit' and data[i][6] != 'Received':
            print("Caution! The payment status should be either in transition or received")
            exit()
        if data[i][7] != 'F' and data[i][7] != 'T':
            print("Caution! The status of delivery should be either true or false")
            exit()
        # if there are more than 9 goods in the order
        while length > 9:
            # read the corresponding goods
            goodsList.append(items[(index * 9):((index + 1) * 9)])
            # lastOrderNum, staffNum, itemNum
            newOrder = OrderNum(lastOrderNum, data[i][1], 9)
            lastOrderNum = str(newOrder)
            orderGoods = []
            for j in goodsList[count]:
                # remove space behind comma
                identity = j.rsplit(" ", 1)[0]
                # if is goods number
                if identity.isdigit():
                    theGood = copyGoods(matchNumber(identity, totalGoodsList))
                # if is goods name
                else:
                    # do the deep copy
                    theGood = copyGoods(matchName(identity, totalGoodsList))
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

        # if remain goods less than 9
        if length > 0:
            goodsList.append(items[(index * 9):])
            try:
                # lastOrderNum, staffNum, itemNum
                newOrder = OrderNum(lastOrderNum, data[i][1], len(goodsList[count]))
                lastOrderNum = str(newOrder)
                orderGoods = []
                for j in goodsList[count]:
                    identity = j.rsplit(" ", 1)[0]
                    if identity.isdigit():
                        theGood = copyGoods(matchNumber(identity, totalGoodsList))
                    else:
                        theGood = copyGoods(matchName(identity, totalGoodsList))
                    theGood.setQuan(j.rsplit(" ", 1)[1])
                    orderGoods.append(theGood)
            except ValueError:
                print(ValueError)
                print("Please check your data in last order number, staff number and item number. It cannot be empty or"
                      " in wrong format")
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
    """Print the last order number into the file

    Args:
        orderList (list): the list storing all orders
        pathL (str): the path to print. Defaults to "zzyTest/OutputLastOrderFile.txt".
    """
    file = open(pathL, "w")
    file.write(orderList[-1].getOrderNumber())
    file.close()


def printAuditedFile(orderList, pathA="zzyTest/OutputAuditedFile.txt"):
    """This is the print function will create or overwrite the text document with the audited information

    Args:
        orderList (list): the list storing all orders
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
    """This prints out all orders' information with a loop

    Args:
        orderList (list): the list storing all orders
    """
    for i in orderList:
        print("-------------------------------------------------------------------------\n")
        print(i)


def printAllUnComplete(orderList):
    """This prints out all the uncompleted orders

    Args:
        orderList (list): the list storing all orders
    """
    for i in orderList:
        if str(i.getComplete()) == "-1":
            print("-------------------------------------------------------------------------\n")
            print(i)


def searchOrder(orderNum, orderList):
    """This can be used to search for an order according to the input order number.
       If found, print out. If not, print error message.

    Args:
        orderNum (string): the order number to search
        orderList (list): the list storing all orders
    """
    for i in orderList:
        if str(i.getOrderNumber()) == orderNum:
            print(i)
            return
    print("The Order Number " + orderNum + " is not found")


def printCustomerList(customerList, pathC="zzyTest/OutputCustomerFile.txt"):
    file = open(pathC, "w")
    file.write("%-25s %d\n" % ("Number_of_customers", len(customerList)))
    file.write("%-25s %s\n" % ("Customer Name", "Customer Address"))
    file.write("---------------------\n")
    for i in range(len(customerList)):
        file.write("%-25s %s\n" % (customerList[i].getName(), customerList[i].getAddress()))
    file.close()


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

    """
    Read user input to select the operations
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
                        "10. Prepare customer list for logistic company\n"
                        "11. Exit\n")

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
        path = input("Please input the expect path, "
                     "if you input -1, the path will be default: zzyTest/OutputCustomerFile.xlsx\n")
        if path == "-1":
            path = "zzyTest/OutputCustomerFile.txt"
        try:
            printCustomerList(theCustomerList, path)
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

    elif instruction == "11":
        isExit = True
    else:
        print("Invalid input instruction number, please check!")
