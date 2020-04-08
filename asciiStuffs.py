# Rob Durst @ 2020
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