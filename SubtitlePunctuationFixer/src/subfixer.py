'''
Created on Apr 20, 2015

Usage: python subfier.py <subtitle file>

@author: Matan Keidar
'''

import os.path
import codecs
import sys

INPUT_ENCODING = "windows-1255"
OUTPUT_ENCODING = "windows-1255"

prefixPunctuation = { '-', '.', '?', '!', ',', '"', ':' }
suffixPunctuation = { '-', '.', '?', '!', ',', '"', ':' }
styleTags = {'<i>', '<b>', '</i>', '</b>'}

def calcOutputFileName(filename):
    rawFile, ext = os.path.splitext(filename)
    return rawFile + '.heb' + ext


def splitPrefix(line):
    prefix = ""
    while line:
        currChar = line[0]
        if currChar not in prefixPunctuation:
            break
        
        prefix += currChar;
        line = line[1:]
    
    return prefix, line


def splitSuffix(line):
    suffix = ""
    
    for c in line[::-1]:
        if c in suffixPunctuation:
            suffix += c
            line = line[:-1]
        else:
            break;
    
    return line, suffix    
    
def fixStyleTags(line):
    styleStart = ''
    styleEnd = ''
    
    if line[0:3] in styleTags:
        styleStart = line[0:3]
        styleEnd = line[-4:-1]
        
        line = line[3:]
        
        if line[-4:-1] not in styleTags and line[-5:-1] not in styleTags:
            styleEnd = styleStart[0] + '/' + styleStart[1:]
        else:
            # split by end tag
            line = line[:-4]    
#             line += styleEnd    
        
    return line, styleStart, styleEnd

if __name__ == '__main__':
    
    # get subtitle input file
    if len(sys.argv) == 1:
        inputFileName = raw_input("enter subtitle file to convert: ")
    else:
        inputFileName = sys.argv[1]
    
    # output file 
    outputFileName = calcOutputFileName(inputFileName)
    outputFile = codecs.open(outputFileName, encoding=OUTPUT_ENCODING, mode="w")
    
    f = codecs.open(inputFileName, encoding=INPUT_ENCODING, mode="r")
    
    # scan each line in subtitle file
    for line in f.readlines():
        line = line.strip()
        
        # detect paragraph in .srt file
        if not line:
            outputFile.write("\r\n")
            continue        
        
        # fix styling tags
        line, styleStart, styleEnd = fixStyleTags(line)

        # fix punctuation
        prefix, line = splitPrefix(line)
        line, suffix = splitSuffix(line)
        
        # merge all extracted parts in correct order
        result = styleStart + suffix + line + prefix + styleEnd
        outputFile.write(result + "\r\n")
    
    print "converted subtitle file:", outputFileName
    print "bye bye.."