from main import *

customerList = readCustomer("zzyTest/Customer.xlsx")
# for i in customerList:
#     print(str(i))

staffList = readStaff("zzyTest/Staff.xlsx")
# for i in staffList:
#     print(str(i))



totalGoodsList = readGoods("zzyTest/Goods.xlsx")
# for i in totalGoodsList:
#     print(str(i))

orderList = readOrder("zzyTest/Order.xlsx", totalGoodsList, customerList)
for i in range(len(orderList)):
    print(str(orderList[i]))