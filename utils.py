# @robertDurst @ 2020
# Helpful utility methods
def binToDec(num):
    return int(num, 2)

def decToBin(num):
    binary =  bin(num).replace("0b", "")
    while len(binary) < 8:
        binary = "0" + binary

    return binary

def encodeASCII(str):
    byteStr = ""
    for c in str:
        ascii = ord(c)
        byteStr += decToBin(ascii)
    return byteStr

def processStringToBytes(someString):
    bs = bytearray()
    # make sure to pack 8 per byte!
    for i in range(0, len(someString), 8):
        bs.append(int(someString[i:i+8], 2))
    return bs

def writeBytesToFile(someString, filename):
    bytess = processStringToBytes(someString)
    newFile = open(filename, "wb")
    newFile.write(bytess)

# much help with de coding from here:
# https://bhrigu.me/blog/2017/01/17/huffman-coding-python-implementation/
def bytesToString(file):
    bitString = ""
    byte = file.read(1)
    while(byte):
        byte = ord(byte)
        bits = bin(byte)[2:].rjust(8, '0')
        bitString += bits
        byte = file.read(1)
    return bitString

def readBytesFromFile(filename):
    newFile = open(filename, "rb")
    return bytesToString(newFile)

# basic binary tree node representation
class Node:
    def __init__(self, data=None, left=None, right=None):
        self.data = data
        self.right = right
        self.left = left