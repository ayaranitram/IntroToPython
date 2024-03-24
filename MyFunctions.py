#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 21:23:27 2019
@author: martin

routines to read keywords in eclipse style
"""

ZeroArgumentsKeywords = (
    'RUNSPEC','GRID','EDIT','PROPS','REGIONS','SOLUTION','SUMMARY','SCHEDULE',
    'ECHO','NOECHO','ENDBOX','NONNC',
    'OIL','WATER','GAS','DISGAS','VAPOIL','FIELD','METRIC',
    'FMTOUT','FMTIN','UNIFOUT','UNIFIN','MULTOUT','MULTIN',
    'IMPLICIT',
    'END',
    'ALL',
    'MSUMLINS'
    'MSUMNEWT',
    'SEPARATE'
    )

def readKeyword( filename ):
    """
    loadInput.readKeyword extracts the keywords and values from a given
    path/filename of an eclipse compatible data file or include and return
    a dictionary containing the keyword and its values inside a list:

        { 'PERMX' : [ 0.0 , 0.0 , 536.2 , 1324.45 , ... , 30.7 , 0 ] }

    HIGHLIGHTS: by default
        > keywords with no arguments will be ignored
        > repeated keywords will be overriten and only the last entry of
          the keyword will be returned.

    To avoid this behaviour please use the function readData.simulationModel
    """
    keywords = {}
    file = open(filename,'r')
    entirefile = file.readlines()
    file.close()

    ignoredKeywords = ZeroArgumentsKeywords

    keywordsIndex = []

    keywordFlag = False
    for line in entirefile :
        if len(line) > 0 :
            values = line.split()
            if len(line) >= 2 and len(values) >= 1 and values[0][:2] == '--' :
                pass # comment line
            elif len(line) >= 1 and len(values) >= 1 and values[0][0] == '/' :
                keywordFlag = False
                keywords[keywordName] = keywordValues.split()
            elif keywordFlag == True :
                counter1 = counter1 + 1
                counter2 = counter2 + 1
                if '--' in line :
                    line = line[:line.index('--')]
                    values = line.split()
                if '/' in line :
                    if line.index('/') > 0 :
                        keywordValues = keywordValues + ' ' + line[:line.index('/')]
                    keywordFlag = False
                    keywords[keywordName] = keywordValues.split()
                else :
                    keywordValues = keywordValues + ' ' + line
            elif len(line) >= 1 and len(values) >= 1 :
                keywordFlag = True
                keywordName = str(values[0])
                keywordValues = ''
                counter1 = 0
                counter2 = 0
                for ignored in ignoredKeywords :
                    if keywordName == ignored :
                        keywordFlag = False
                        keywords[keywordName] = None
                        break
            else :
                pass #empty line

    return keywords

def expandKeyword( keywordValues , expandDefaults=True) :
    """
    expandKeyword receives list of values or a space-separated string containing
    the values of the property keyword in the compressed format ' 3*0.257 ' and
    returns the expanded ' 0.257 0.257 0.257 ' property as a list or
    space-separated string according to the format of the received input.

    the optional argument speak controls the verbosity of expandKeyword, where:
        0 = not ouptut at all
        1 = print every message
        2 = print final statement only
    """
    if keywordValues == None :
        return ''

    if type(keywordValues) == list :
        outformat = 'list'
        try :
            inputValues = ' ' + ' '.join(keywordValues) + ' '
        except :
            inputValues = ' ' + ' '.join(list(map(str,keywordValues))) + ' '
    elif type(keywordValues) == str :
        outformat = 'str'
        
        inputValues = ' ' + keywordValues + ' '
        inputValues = inputValues.replace('\n',' ')
        inputValues = inputValues.replace('/',' /')
    else :
        raise Exception('keyword values to be expanded should be provided as LIST or STRING')
    outputValues = ''
    ini = 0
    end = len(inputValues)
    starFlag = '*' in inputValues[ini:]
    prog = 100*ini//end

    while starFlag :

        star = inputValues[ini:].index('*')
        star = star + ini
        starIni = inputValues[star::-1].index(' ')
        starIni = star - starIni + 1
        starEnd = inputValues[star:].index(' ')
        starEnd = star + starEnd

        temp = ' '
        rept = inputValues[star+1:starEnd]
        inte = inputValues[starIni:star]
        if len(inte) == 0 :
            inte = '1'
        if len(rept) > 0 :
            inte = int(inte)
            for i in range(inte) :
                temp = temp + ' ' + rept
            outputValues = outputValues + ' ' + inputValues[ini:starIni] + temp + ' '
        else:
            if expandDefaults == True :
                inte = int(inte)
                rept = '1*'
                for i in range(inte) :
                    temp = temp + ' ' + rept
                outputValues = outputValues + ' ' + inputValues[ini:starIni] + temp + ' '
            else :
                outputValues = outputValues + ' ' + inputValues[ini:starEnd] + ' '

        ini = starEnd
        starFlag = '*' in inputValues[ini:]
        if prog < 100*ini//end :
            prog = 100*ini//end

    outputValues = outputValues + ' ' + inputValues[ini:]

    outputValues = outputValues.split()
    if outformat == 'str' :
        outputValues = ' ' + ' '.join(outputValues) + ' '

    return outputValues