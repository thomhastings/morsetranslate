#morsetranslator.py
#translate strings to and from morse code notation

class MorseTranslator(object):

    _alphabet = {
        'A':'.-',
        'B':'-...', 
        'C':'-.-.',
        'D':'-..',
        'E':'.',
        'F':'..-.',
        'G':'--.',
        'H':'....',
        'I':'..',
        'J':'.---',
        'K':'-.-',
        'L':'.-..',
        'M':'--',
        'N':'-.',
        'O':'---',
        'P':'.--.',
        'Q':'--.-',
        'R':'.-.',
        'S':'...',
        'T':'-',
        'U':'..-',
        'V':'...-',
        'W':'.--',
        'X':'-..-',
        'Y':'-.--',
        'Z':'--..',
        '1':'.----',
        '2':'..---',
        '3':'...--',
        '4':'....-',
        '5':'.....',
        '6':'-....',
        '7':'--...',
        '8':'---..',
        '9':'----.',
        '0':'-----',
        '.':'.-.-.-',
        ',':'--..--',
        '?':'..--..',
        '\'':'.----',
        '!':'-.-.--',
        '/':'-..-.',
        '(':'-.--.',
        ')':'-.--.-',
        '&':'.-...',
        ':':'---...',
        ';':'-.-.-.',
        '=':'-...-',
        '+':'.-.-.',
        '-':'-....-',
        '_':'..--.-',
        '\"':'.-..-.',
        '$':'...-..-',
        '@':'.--.-.'
        
        }
    
    def convertToMorse(self, inStr):
        
        """Convert a string of plain text into morse notation"""
        
        #no distinction between cases in morse so convert to upper for ease
        #of lookup in morse alphabet dict
        inStr = inStr.upper()

        #break inStr into discrete words
        wordList = inStr.split()

        outStr = ""

        #need the index of both the wordList and each word itself in order
        #to check if we're at the last word/character thus the enumerate()
        for wcount,w in enumerate(wordList):
            for ccount, c in enumerate(w):

                #if the character is not representable in morse just copy 
                #the character as is into the outStr
                if c in MorseTranslator._alphabet:
                    outStr += MorseTranslator._alphabet[c]
                else:
                    outStr += c

                #add a space if c is not the last character in word w
                #remember, in morse notation the ' ' character is used to 
                #seperate characters and '/' will be used to seperate words
                #this check avoids adding an extra trailing space to the last 
                #character in a word
                if ccount != len(w) - 1:
                    outStr += " "
            
            #moving on to next word, add the ' / ' string which
            #we're using to represent a space between morse words
            if wcount != len(wordList) - 1:
                outStr += " / "

        return outStr

    def convertFromMorse(self, inStr):

        """Convert a string of morse notation into plain text. Non morse 
        symbols(anything other than '.' or '-') are copied into the output 
        string as is."""
        
        #break the morse notation string up into seperate words
        #since morse notation uses " " between characters
        #'/' is used to signify a break between words
        wordList = inStr.split("/")

        outStr = ""

        for wcount, w in enumerate(wordList):

            #get a list of each morse character string (represented by several
            #dots and dashes) that makes up word w
            charList = w.split()
            
            #lookup the plaintext character for each morse character string
            for c in charList:
                foundKey = [
                k for k,v in MorseTranslator._alphabet.items() if v == c]

                if foundKey:
                    outStr += foundKey[0]
                else:
                    outStr += c

            #add a space after each word except if it's the last word
            if wcount != len(wordList) - 1:
                outStr += " "

        return outStr
