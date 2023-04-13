import random
class OrderNum(object):
    def calDigitNum(self):
        sum = 0
        for i in range(len(str(self.staffNum))):
            sum += int(str(self.staffNum)[i]) * int(str(self.seqNum)[i])
        modulusNum = self.getModulusNum()
        for i in range(10):
            if (sum + i) % modulusNum == 0:
                return i

    def getModulusNum(self):
        if self.modulusChar == "A":
            return 7
        if self.modulusChar == "B":
            return 8
        if self.modulusChar == "C":
            return 9

    def nextChar(self, alphabet):
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
        return random.choice('ABC')

    def getAlphabet(self):
        return self.alphabet

    def getStaffNum(self):
        return self.staffNum

    def getModulusChar(self):
        return self.modulusChar

    def getSeqNum(self):
        return self.seqNum

    def getItemNum(self):
        return self.itemNum

    def getCheckDigit(self):
        return self.checkDigit

    def getWholeNum(self):
        return str(self.alphabet) + str(self.staffNum) + str(self.modulusChar) + str(self.seqNum) + str(self.itemNum) + str(self.checkDigit)

    def __str__(self):
        return str(self.alphabet) + str(self.staffNum) \
               + str(self.modulusChar) + str(self.seqNum) + str(self.itemNum) + "(" + str(self.checkDigit) + ")"

    def __init__(self, lastOrderNum, staffNum, itemNum):
        self.lastOrderNum = lastOrderNum
        self.alphabet, self.seqNum = self.calNumber()
        self.staffNum = staffNum
        self.modulusChar = self.randModulusChar()
        self.itemNum = itemNum
        self.checkDigit = self.calDigitNum()


