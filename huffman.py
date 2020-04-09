# @robertDurst @ 2020
# Implementation of Huffman Coding:
# https://en.wikipedia.org/wiki/Huffman_coding
from collections import Counter
from utils import encodeASCII, decToBin, binToDec, writeBytesToFile, readBytesFromFile, Node

"""
    A completely compressed file is formatted as so:
    [padding length][header][encodeding][padding]
"""
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
        keyNode1, val1 = freqToNode[index[0]].pop(0), index[0]

        # check if index has more, if not delete
        if len(freqToNode[val1]) == 0:
            del freqToNode[val1]
            index.pop(0)

        # grab second value and key
        keyNode2, val2 = freqToNode[index[0]].pop(), index[0]

        # check if index has more, if not delete
        if len(freqToNode[val2]) == 0:
            del freqToNode[val2]
            index.pop(0)

        # comine keys and vals to make a "merged" node
        combinedVal = val1 + val2
        combinedKey = Node(left=keyNode1, right=keyNode2)

        # put it in the list, checking if it is a new node
        if not combinedVal in freqToNode:
            freqToNode[combinedVal] = []
            index.append(combinedVal)
            # make sure to resort since this may not be largest val
            index = sorted(index)

        # now we can add the new node
        freqToNode[combinedVal].append(combinedKey)

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

    headerSansPadding = compressHeader(table)

    # padding length in header is 8 bits so it is not needed for thic
    paddingLen = (8 - len(headerSansPadding + compressedStr) % 8)
    padding = "".join(["0"] * paddingLen)
    header = decToBin(paddingLen) + headerSansPadding 

    return header + compressedStr + padding

"""
    My approach to compressing the header is as follows:
    [key]    : 8 bits normal ascii representation
    [length] : 3 bits, length of the huffman coding bits
    [value]  : 1-8 bits, huffamn coding
"""
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
    # first decompress the header and generate a tree
    [tree, compressed]  = decompressHeader(compressed)

    letters, root, cur = [], tree, tree

    # using the tree, decode each chracter from the given "bit paths"
    for c in compressed:
        cur = (cur.left, cur.right)[c == '1']

        if (cur.data != None):
            letters.append(cur.data)
            cur = root

    return "".join(letters)

# helper for grabbing x bits
def takeBits(compressed, numBits):
    return [compressed[:numBits], compressed[numBits:]]

# helper for generating the tree from the decompressed header. Takes a path and
# creates each of the nodes in the path, finally placing the char at a leaf
def insertIntoTree(tree, data, path):
    cur = tree
    for c in path:
        # "0" --> Left
        if c == "0":
            if not cur.left:
                cur.left = Node()
            cur = cur.left
        # "1" --> Right
        else:
            if not cur.right:
                cur.right = Node()
            cur = cur.right
    # at the end of the path, place character in a leaf node
    cur.data = data

def decompressHeader(compressed):
    # remove padding
    padding, compressed = takeBits(compressed, 8)
    padding = binToDec(padding)
    compressed = compressed[:len(compressed)-padding]

    # determine number of values in tree
    numKlv, compressed = takeBits(compressed, 8)
    numKlv = binToDec(numKlv)

    # decode tree pairs and insert into tree
    tree = Node()
    for _ in range(numKlv):
        k, compressed = takeBits(compressed, 8)
        data = chr(binToDec(k))
        l, compressed = takeBits(compressed, 8)
        path, compressed = takeBits(compressed, binToDec(l))
        insertIntoTree(tree, data, path)

    return [tree, compressed]