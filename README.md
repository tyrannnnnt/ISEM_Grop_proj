# ISEM_Grop_proj

# Group Member:
    Group A
    ZHANG Jiayi     19250568
    CHENG Min Hsiu  19203144
    LIU Yulin       20250541

# Environment:
Please install: **openpyxl, pandas** before you run the program. 
Because the program requires excel input and thus need the openpyxl library. 
You can try "pip install openpyxl" or similar commands.

# Input File Format:
+ The order file:
  + Should be the Excel file(.xlsx) format
  + The order and form of the header is：

    LastOrderNum StaffNumber Items OrderDate CustomerNumber PaymentMethod Payment collection Delivered
+ The customer file:
  + Should be the Excel file(.xlsx) format
  + The order and form of the header is：

    Name Address CustomerNumber MallDollar
+ The goods file:
  + Should be the Excel file(.xlsx) format
  + The order and form of the header is：

    GoodsName GoodsValue GoodsNum cost
+ The staff file:
  + Should be the Excel file(.xlsx) format
  + The order and form of the header is：

    StaffNum

# Possible Output File(txt):
+ Output Last Order File: store the latest order number
+ Output Audited File: store the order information for audited usage
+ Output Customer File: store the customer name and address