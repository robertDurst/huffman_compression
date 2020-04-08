from pathlib import Path
import time
from collections import Counter
from illiad import theBook
from asciiStuffs import encodeASCII, decToBin, binToDec

class Node:
    def __init__(self, data=None, left=None, right=None):
        self.data = data
        self.right = right
        self.left = left

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

# much help with decoding from here:
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

def compress(uncompressed):
    # first count frequencies of each character
    count = Counter(uncompressed)

    # use frequency as index and keep a second index array to keep track of indices
    index = []
    freqToNode = {}
    for k in count:
        v = count[k]
        if not v in freqToNode:
            freqToNode[v] = []
            index.append(v)
        freqToNode[v].append(Node(data=k))

    # sort in ascending order
    index = sorted(index)

    # continuously merge until one node remains
    while len(index) > 1 or len(freqToNode[index[0]]) > 1:

        # grab first value and key
        key_node_1, val_1 = freqToNode[index[0]].pop(0), index[0]

        # check if index has more, if not delete
        if len(freqToNode[val_1]) == 0:
            del freqToNode[val_1]
            index.pop(0)

        # grab second value and key
        key_node_2, val_2 = freqToNode[index[0]].pop(), index[0]

        # check if index has more, if not delete
        if len(freqToNode[val_2]) == 0:
            del freqToNode[val_2]
            index.pop(0)

        # comine keys and vals to make a "merged" node
        combined_val = val_1 + val_2
        combined_key = Node(left=key_node_1, right=key_node_2)

        # put it in the list, checking if it is a new node
        if not combined_val in freqToNode:
            freqToNode[combined_val] = []
            index.append(combined_val)
            # make sure to resort since this may not be largest val
            index = sorted(index)

        # now we can add the new node
        freqToNode[combined_val].append(combined_key)

    # perform a recursive, preorder traversal, creating  a table of characters to
    # their bit code
    table = {}
    def traverseTree(tree, byteStr):
        if tree.data != None:
            table[tree.data] = byteStr
            return

        traverseTree(tree.left, byteStr + "0")
        traverseTree(tree.right, byteStr + "1")


    # now with an array formatted tree, we need to create a table for encoding
    tree = freqToNode[index[0]][0]
    traverseTree(tree, "")

    # compress the str
    compressedStr = ""
    for c in uncompressed:
        compressedStr += table[c]

    header_sans_padding = compressHeader(table)

    # padding length in header is 8 bits so it is not needed for thic
    paddingLen = (8 - len(header_sans_padding + compressedStr) % 8)
    padding = "".join(["0"] * paddingLen)
    header = decToBin(paddingLen) + header_sans_padding 

    return header + compressedStr + padding

def compressHeader(table):
    length = decToBin(len(table))
    klv = ""
    for key in table:
        k = encodeASCII(key)
        v = table[key]
        l = decToBin(len(v))
        klv += k + l + v
    return length + klv


def decompress(compressed):
    [tree, compressed]  = decompressHeader(compressed)

    letters, root, cur = [], tree, tree

    for c in compressed:
        cur = (cur.left, cur.right)[c == '1']

        if (cur.data != None):
            letters.append(cur.data)
            cur = root

    return "".join(letters)

def takeByte(bits):
    return [bits[:8], bits[8:]]

def insertIntoTree(tree, data, path):
    cur = tree
    for c in path:
        if c == "0":
            if not cur.left:
                cur.left = Node()
            cur = cur.left
        else:
            if not cur.right:
                cur.right = Node()
            cur = cur.right
    cur.data = data

def decompressHeader(compressed):
    # remove padding
    padding, compressed = takeByte(compressed)
    padding = binToDec(padding)
    compressed = compressed[:len(compressed)-padding]

    # determine number of values in tree
    numKlv, compressed = takeByte(compressed)
    numKlv = binToDec(numKlv)

    # decode tree pairs and insert into tree
    tree = Node()
    for _ in range(numKlv):
        k, compressed = takeByte(compressed)
        data = chr(binToDec(k))
        l, compressed = takeByte(compressed)
        path = compressed[:binToDec(l)]
        compressed = compressed[binToDec(l):]
        insertIntoTree(tree, data, path)

    return [tree, compressed]