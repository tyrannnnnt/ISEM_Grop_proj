class OrderNum(object):
    def calDigitNum(self):
        sum = 0
        for i in range(len(self.staffNum)):
            sum += int(self.staffNum[i]) * int(self.seqNum[i])
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
        return self.alphabet + self.staffNum + self.modulusChar + self.seqNum + self.itemNum + self.checkDigit

    def __init__(self, alphabet, staffNum, modulusChar, seqNum, itemNum):
        self.alphabet = alphabet
        self.staffNum = staffNum
        self.modulusChar = modulusChar
        self.seqNum = seqNum
        self.itemNum = itemNum
        self.checkDigit = self.getCheckDigit()
