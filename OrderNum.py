"""
Group A member:
CHENG MIN HSIU  19203144
ZHANG Jiayi     19250568
LIU Yulin       20250541
This file including the Class of OrderNum which contains the information which should be stored in the order number.
Includes the functions of calculating the next order number, picking random modulus Character and other specific
functions.
"""

import random


class OrderNum(object):
    """
    The OrderNum Class containing the information of the order number. It contains the function of calculating the next
    order number and check digit number and randomly picking the modulus character.
    """

    def calDigitNum(self):
        """
        This function will calculate the check digit according to the modulus number

        Returns:
            int: check digit
        """
        sum = 0
        for i in range(len(str(self.staffNum))):
            sum = sum + int(str(self.staffNum)[i]) * int(str(self.seqNum)[i])
        modulusNum = self.getModulusNum()
        for i in range(10):
            if (sum + i) % modulusNum == 0:
                return i

    def getModulusNum(self):
        """
        This function is used to get the corresponding modulus number according to the modulus character.

        Returns:
            int: the modulus number
        """
        if self.modulusChar == "A":
            return 7
        if self.modulusChar == "B":
            return 8
        if self.modulusChar == "C":
            return 9

    def nextChar(self, alphabet):
        """
        This function determines the character at the beginning of the order number.
        If it hasn't reached Z, return next letter of the alphabet. If Z, then start with AA. If ZZ, return A

        Args:
            alphabet (alphabet): input the alphabet part of the order number

        Returns:
            String: single letter or paired letters
        """
        if len(alphabet) == 1:
            if alphabet != "Z":
                return chr(ord(alphabet) + 1)
            else:
                return "AA"
        elif len(alphabet) == 2:
            if alphabet != "ZZ":
                return alphabet[0] + chr(ord(alphabet[1]) + 1)
            else:
                return "A"

    def calNumber(self):
        """
        This function can calculate the order number of the next order

        Returns:
            string: next order number
        """
        alphabet = ""
        digitPart = ""
        # single alphabet
        if len(self.lastOrderNum) == 18:
            alphabet = self.lastOrderNum[0]
            digitPart = self.lastOrderNum[8:14]
        # double alphabet
        elif len(self.lastOrderNum) == 19:
            alphabet = self.lastOrderNum[0:2]
            digitPart = self.lastOrderNum[9:15]
        else:
            print("Invalid last order number! " + self.lastOrderNum)
            return -1, -1
        if digitPart != 999999:
            return alphabet, str(int(digitPart) + 1)
        else:
            return self.nextChar(alphabet), "000001"

    def randModulusChar(self):
        """
        This function picking a modulus character randomly

        Returns:
            string: the modulus number
        """
        return random.choice('ABC')

    def getAlphabet(self):
        """
        Get the alphabet

        Returns:
            alphabet
        """
        return self.alphabet

    def getStaffNum(self):
        """
        Get the staff number

        Returns:
            int: staff number
        """
        return self.staffNum

    def getModulusChar(self):
        """
        Get the modulus character

        Returns:
            char: modulus character
        """
        return self.modulusChar

    def getSeqNum(self):
        """
        Get the order number

        Returns:
            string: order number
        """
        return self.seqNum

    def getItemNum(self):
        """
        Get the item number

        Returns:
            string: item number
        """
        return self.itemNum

    def getCheckDigit(self):
        """
        Get the check digit

        Returns:
            int: check digit
        """
        return self.checkDigit

    def getWholeNum(self):
        """
        Get the invoice order number

        Returns:
            string: order number
        """
        return str(self.alphabet) + str(self.staffNum) + str(self.modulusChar) + str(self.seqNum) + \
               str(self.itemNum) + str(self.checkDigit)

    def __str__(self):
        """The order number in correct order and format

        Returns:
            string: order number
        """
        return str(self.alphabet) + str(self.staffNum) \
               + str(self.modulusChar) + str(self.seqNum) + str(self.itemNum) + "(" + str(self.checkDigit) + ")"

    def __init__(self, lastOrderNum, staffNum, itemNum):
        """
        Initialize the class base on the input parameters
        """
        self.lastOrderNum = lastOrderNum
        self.alphabet, self.seqNum = self.calNumber()
        self.staffNum = staffNum
        self.modulusChar = self.randModulusChar()
        self.itemNum = itemNum
        self.checkDigit = self.calDigitNum()
