import argparse
import sys

from PartA import Tokenizer

#0(n+m) time depending on fileA and fileB size
def intersectCount(fileA, fileB):
    #use part A to tokenize both files
    tokenizerA = Tokenizer(fileA)
    tokenizerB = Tokenizer(fileB)
    #finding the set intersection
    print(len(set(tokenizerA.tokenize()) & set(tokenizerB.tokenize())))

def main():
    try:
        fileA = sys.argv[1]
        fileB = sys.argv[2]
        intersectCount(fileA, fileB)
    except Exception as e:
        print("An error occured: " + str(e))

if __name__ == "__main__":
    main()