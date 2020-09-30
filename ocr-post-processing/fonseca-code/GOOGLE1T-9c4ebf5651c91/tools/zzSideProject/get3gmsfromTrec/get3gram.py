# -*- coding: utf-8 -*-
"""
Jorge.FonsecaCacho@UNLV.edu
"""

import sys
#Check Argument amount is right
if len(sys.argv) != 3:
    print "Usage: get3gram.py OCROutputFile.output OCRFile.clean"
    quit()
#print sys.argv[0] #Prints the Name of the File pwd/Filename
#print sys.argv[1] #Prints .output
#print sys.argv[2] #Prints .clean
print "Program will open OCRSpell output file and find for all entries the preceding word and the word after along with line/word number"


fileout   = sys.argv[1]
fileclean = sys.argv[2]

#Read in the file.output line by line
outlines = [line.rstrip('\n') for line in open(fileout)]

#Read in the file.clean line by line
#cleanlines = [line.rstrip('\n') for line in open(fileclean)]

#Read file with OCR'd Text
with open(fileclean, 'r') as myfile:
    words=myfile.read().replace('\n', '')
words = words.split() #split line into parts
words = [x for x in words if x != ')']  #Remove all entries with just a parenthesis for cleanup
words = [x for x in words if x != '.']  #Remove all entries with just a period for cleanup
print "Number of words in OCR'd.clean file:", len(words)

#Open a file to write a copy of our 3grams
fout = open(fileout+".3gms", 'w')
#fout.write("@3gms Output of File: "+fileout+"\n")


TotalWords = len(outlines)
print "Total Words parsed in OCRSpell File:", TotalWords
print outlines[0]

currentWord = 0;
#Main Loop:
print "Starting to process..."
for currentLine in outlines[1:]:   
    #print "Line:", currentLine
    if currentLine[0] == "*":
        print "Word was marked as correct by OCRSpell, skipping"
        currentWord +=1  #Don't Forget to increment   
        continue
    if currentLine[0] == "&" or currentLine[0] == "#": #This is a given but check to be safe
        parts = currentLine.split() #split line into parts

        #Skip numbers as they are not 'misspellings'
        if parts[1].isdigit():
            print "Entry:", parts[1], "is a number. Skipping"
            currentWord +=1  #Don't Forget to increment
            continue
        
        #Print Mispelled Word
        print "Mispelled Word: '"+parts[1]+"' At Word Position:", currentWord
        #Print The Word from OCR File at that position (and hope they match)
        print "Position in OCRSpell File word:", words[currentWord]
#        print parts[1], "-", words[currentWord] #Simplified version
        
        #If they don't match we need to search ahead and before, but for now we can go on as it seems okay, keep check so
        #when we run into this issue we are at least made aware.
        if  parts[1] != words[currentWord]:
            print "Warning: Words do not match, something is unaligned and needs alignment!"
        
        #For now since they match lets get the word before and after it , print it here and to our output file
        
        if currentWord < 1 or currentWord+1 >= len(words): #beginning or end so we can't get surrounding words for 3gms
            print "Skipped one"
            fout.write("* "+ parts[1])
            currentWord +=1
            continue
            
        #Normal Case:
        print "Word Before: '"+words[currentWord -1 ]+"' Word After: '"+words[currentWord+1]+"' Location:",currentWord
        print words[currentWord -1 ], parts[1], words[currentWord+1], str(currentWord)#equivalent written to file
        fout.write(words[currentWord -1 ]+" "+parts[1]+" "+words[currentWord+1]+" "+str(currentWord)+"\n")
        #If we want to store the position of word:
#        fout.write(words[currentWord -1 ]+" "+parts[1]+" "+words[currentWord+1]+" "+currentWord+"\n")
    
#    if currentWord > 10: break #temporary to not process full file until code is done

    currentWord +=1        
print "Out of main For Loop"    
    
#print currentWord
#print currentLine

"""
What we want is to take FR9401040.0.output and for each entry that is not a number, we want to find the word before it and after.
We then want to output a file that has format:


number word1 wordd2 word3

number is the location in text (to add later on)

word1 and word3 are surrounding words

word22 is our misspelled word

"""
#fileout.close()
#fileclean.close()
fout.close()
print "End"