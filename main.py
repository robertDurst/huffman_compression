# @robertDurst @ 2020
# Example execution, encoding and decoding of the Illiad (uncompressed.txt)
import time
from pathlib import Path
from utils import encodeASCII
from main import writeBytesToFile, compress, readBytesFromFile, decompress

def bitsToKb(bits):
    kb = float(bits) / 1000
    return str(round(kb, 2))

def performAndAnalyze(uncompressedFilename, compressedFilename, compressedASCIIFilename):
    DATA = open(uncompressedFilename, "r").read()

    before = time.time()
    encodedHuffman = compress(DATA)
    writeBytesToFile(encodedHuffman, compressedFilename)
    afterEncH = time.time()

    encodedASCII = encodeASCII(DATA)
    writeBytesToFile(encodedASCII, compressedASCIIFilename)
    afterEncA = time.time()
    
    decoded = decompress(readBytesFromFile(compressedFilename))
    print("Decoded first 1000 characters:\n\n", decoded[:1000], "\n")
    afterDec = time.time()

    sizeASCII = Path(compressedASCIIFilename).stat().st_size
    sizeHuffman = Path(compressedFilename).stat().st_size
    sizeUncompressed = Path(uncompressedFilename).stat().st_size
    compressed = float(sizeHuffman) / float(sizeUncompressed) * 100
    print("Compressed size: " + str(round(compressed, 2)) + "% of original")
    print("Size of huffman compressed file: " + bitsToKb(sizeHuffman) + "kb")
    print("Size of ascii compressed file: " + bitsToKb(sizeASCII) + "kb")
    print("Size of  uncompressed file: " + bitsToKb(sizeUncompressed) + "kb")
    print("Time to encode Huffman:", afterEncH - before)
    print("Time to encode ASCII:", afterEncA - afterEncH)
    print("Time to decode Huffman:", afterDec - afterEncA)

performAndAnalyze("uncompressed.txt", "compressed_huffman", "compressed_ascii")