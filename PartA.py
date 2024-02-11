import re
import argparse
import sys
from typing import *


Token = str
Count = int
Frequencies = Dict[Token, Count]

class Tokenizer:
    #0(1) time because it always just initializes
    def __init__(self, fileA):
        self.inputFileName = fileA
        return

    #0(n) time depending on how many lines long the file input is
    def tokenize(self):
        tokens = []
        #read the file
        with open(self.inputFileName, 'r') as file:
            for line in file:
                #get alphanumeric only and lower case
                alphanumericOnly = re.compile(r'[^a-zA-Z0-9]')
                alphanumericString = alphanumericOnly.sub(' ', line)
                #split by blankspace
                lowerCaseStrings = alphanumericString.lower().split()
                for eachString in lowerCaseStrings:
                    tokens.append(eachString)
        return tokens

    #O(n) time depending on how long the token list is
    def compute_word_frequencies(self, tokens):
        frequency = {}
        #iterating through token list
        for eachToken in tokens:
            if eachToken in frequency:
                #adding a count to dict value if it occurs
                frequency[eachToken] = frequency[eachToken] + 1
            else:
                frequency[eachToken] = 1
        return frequency

    #O(nlogn) for sorting and O(n) time depending on how long the frequencies dict is
    def print_frequencies(self, frequencies):
        #sort frequencies by value size
        sortedFrequencies = sorted(frequencies.items(), key=lambda item: item[1], reverse=True)
        size = len(sortedFrequencies)
        index = 0
        #going through all the sorted frequencies and keeping track of the index after as well
        while index < size:
            currentKey = sortedFrequencies[index][0]
            currentValue = sortedFrequencies[index][1]
            keys = [currentKey]
            updatedIndex = index + 1
            # if multiple value sizes are the same as each other
            # save them to a list, and then sort them alphabetically by key
            while (updatedIndex < size and currentValue == sortedFrequencies[updatedIndex][1]):
                keys.append(sortedFrequencies[updatedIndex][0])
                updatedIndex += 1
            keys.sort()
            for eachKey in keys:
                value = frequencies[eachKey]
                print(eachKey + " = " + str(value))

            index = updatedIndex


def main():
    try:
        fileA = sys.argv[1]
        tokenizer = Tokenizer(fileA)
        tokens = tokenizer.tokenize()
        frequency = tokenizer.compute_word_frequencies(tokens)
        tokenizer.print_frequencies(frequency)
    except Exception as e:
        print("An error occured: " + str(e))



if __name__ == "__main__":
    main()