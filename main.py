# -----------------------------------------------------------------------------------
#                             CMSC 124 MACHINE PROBLEM
#                           Fernandez, Chien Carisse P.
# -----------------------------------------------------------------------------------

connectives = ['AND', 'OR', 'IMPLIES', 'EQUIVALENT','NOT']
atomicSentence = ['TRUE', 'FALSE', 'P', 'Q', 'R']
specialCharacters = ['(',')',';']
specialChar = ['(',')']                     # open and close parentheses only
specialCharNames = {                        # dictionary of special characters
    ";" : "SEMICOLON",
    "(" : "LEFT PARENTHESIS",
    ")" : "RIGHT PARENTHESIS"
}
connectiveNames = {
    "AND" : "LOG AND OP",
    "OR" : "LOG OR OP",
    "IMPLIES" : "LOG IMPLICATION OP",
    "EQUIVALENT" : "LOG EQUIVALENCE OP",
    "NOT" : "LOG NEG OP"
}
# -----------------------------------------------------------------------------------
#                      CHECK IF THE SENTENCE IS ATOMIC
# -----------------------------------------------------------------------------------
def checkAtomic(sentence):
    sentence = sentence.strip(";")
    if sentence in atomicSentence:
        return True
    else:
        return False

# -----------------------------------------------------------------------------------
#                  RETURN A LIST OF LEXEMES IN THE SENTENCE
# -----------------------------------------------------------------------------------
def getLexemes(sentence):
    lexemes = []
    tempLexeme = ""

    for character in sentence:
        if character in specialCharacters:
            if tempLexeme != "":
                lexemes.append(tempLexeme)
            lexemes.append(character)
            tempLexeme = ""
        elif character == " ":
            lexemes.append(tempLexeme)
            tempLexeme = ""
        else:
            tempLexeme = tempLexeme + character
    lexemes = list(filter(None, lexemes))
    return lexemes
# -----------------------------------------------------------------------------------
#              CHECK THE SYNTAX OF THE CODE AND PRINT ERROR MESSAGE
# -----------------------------------------------------------------------------------
def checkSyntax(sentence):
    flag = True

    # check if sentence has balanced set(s) of parentheses
    balance = 0
    for character in sentence:
        if character == "(":
            balance += 1
        elif character == ")":
            balance -= 1
    if balance != 0:
        print("SYNTAX ERROR AT LINE " + sentence +"\n[Sentence has an unbalanced set of parentheses]")
        return False

    # check if sentence ends with ;
    if sentence[-1] != ";":
        print("SYNTAX ERROR AT LINE " + sentence +"\n[No semicolon(;) found at the end of line]")
        return False


    # check if the sentence ends in a connective
    lexemes1 = getLexemes(sentence)
    lexemes1.pop()                   # remove ';' from list
    if lexemes1.pop() in connectives:
        print("SYNTAX ERROR AT LINE " + sentence +" \n[Sentence ends with a connective]")
        return False

    # check if sentence inside a parenthesis ends in a connective
    # eg. P AND Q IMPLIES
    for index, lex in enumerate(lexemes1):
        if (index + 1 < len(lexemes1) and index - 1 >= 0):    # check index bounds
            if str(lex) == ")":
                if lexemes1[index-1] in connectives:
                    print("SYNTAX ERROR AT LINE " + sentence + "\n[Sentence inside a parenthesis ends with a connective]")
                    return False

    # check if lexeme is acceptable as a token
    lexemes = getLexemes(sentence)
    lexemes.pop()               # remove ; at the end (used to see if there is
    acceptableLex = 0           # a duplicate ; in each sentence)
    for lexeme in lexemes:
        if lexeme in connectives:
            acceptableLex += 1
        elif lexeme in atomicSentence:
            acceptableLex += 1
        elif lexeme in specialChar:
            acceptableLex += 1

    if len(lexemes) != acceptableLex:
        print("SYNTAX ERROR AT LINE: "+ sentence +"\n[Invalid lexeme found]")
        return False

    # when there is only 1 identifiers, the only identifiers acceptable is P
    # when there are 2 identifiers, P and R are the only acceptable identifiers
    lexemes2 = getLexemes(sentence)
    lexemes2.pop()           # remove ; at the end

    ident = []
    for lexeme in lexemes:
        if (lexeme == 'P' and 'P' not in ident) or (lexeme == 'Q' and 'Q' not in ident) or (lexeme == 'R' and 'R' not in ident):
            ident.append(lexeme)
    numOfIdent = len(ident)

    if (numOfIdent == 1) and ('P' not in lexemes2):
        print("SYNTAX ERROR AT LINE: " + sentence + "\n[Wrong ident used. Please use P ident]")
        return False
    if numOfIdent == 2:
        if ('P' not in lexemes2) or ('Q' not in lexemes2):
            print("SYNTAX ERROR AT LINE: " + sentence + "\n[Wrong ident used. Please use P and Q as ident]")
            return False
# -----------------------------------------------------------------------------------
#                       PRINT LEXEMES AND THEIR TOKENS FUNCTION
# -----------------------------------------------------------------------------------
def printTokens(sentence):
    lexemes = getLexemes(sentence)
    token = ""
    for lexeme in lexemes:
        if lexeme == "TRUE" or lexeme == "FALSE":
            token = "CONST"
        elif lexeme in connectives:
            token = connectiveNames[lexeme]
        elif lexeme in specialCharacters:
            token = specialCharNames[lexeme]
        else:
            token = "IDENT"
        print("Next Lexeme:", lexeme, "Token:", token)



# -----------------------------------------------------------------------------------
#                           GROUP BY PARENTHESIS
# -----------------------------------------------------------------------------------
def returnParen(sentence):
    i = sentence[sentence.find('('):sentence.find(')')].count('(')
    groups = sentence[sentence.find('('):].split(')')
    return (')'.join(groups[:i]) + ')')

def groupByParen(sentence):
    flag = False
    count = 0
    for index, lex in enumerate(sentence):
        if(index + 1 < len(sentence)  and index - 1 >= 0):
            if lex == "(":
                flag = True
                count = index

    if flag == True:

        tempSentence = ' '.join(sentence[count:])
        parenSentence = returnParen(tempSentence)
        parenIndex = 0
        for index, lex in enumerate(sentence):
            if (index + 1 < len(sentence) and index - 1 >= 0):
                if lex == "(" :
                    sentence[index] = parenSentence
                    parenIndex = index + 1
        for index, lex in enumerate(sentence[parenIndex:]):
            if (index + 1 < len(sentence) and index - 1 >= 0):
                if lex == ")":
                    closeParenIndex = index + parenIndex + 1


        del sentence[parenIndex  : closeParenIndex]

    return sentence

# -----------------------------------------------------------------------------------
#                      CHANGES THE FORMAT OF IMPLIES OP
# -----------------------------------------------------------------------------------
def changeImplies(sentence):
    for index, lex in enumerate(sentence):
        if(index + 1 <len(sentence)  and index - 1 >= 0):
            if lex == "IMPLIES":
                prevLex = sentence[index - 1]
                nextLex = sentence[index + 1]
                sentence[index] = "not " + prevLex + " or " + nextLex
                sentence.pop(index - 1)
                sentence.pop(index)
    return(sentence)

# -----------------------------------------------------------------------------------
#                      CHANGES THE FORMAT OF EQUIVALENCE OP
# -----------------------------------------------------------------------------------
def changeEquivalence(sentence):
    for index, lex in enumerate(sentence):
        if(index + 1 <len(sentence)  and index - 1 >= 0):
            if lex == "EQUIVALENT":
                prevLex = sentence[index - 1]
                nextLex = sentence[index + 1]
                sentence[index] = "(not " + prevLex + " or " + nextLex + ") and (not " + nextLex + " or " + prevLex + ")"
                sentence.pop(index - 1)
                sentence.pop(index)
    return(sentence)
# -----------------------------------------------------------------------------------
#             RETURN A LIST OF LEXEME GROUPED WHEN THERE IS A NEG OP
# -----------------------------------------------------------------------------------
def groupByNot(sentence):
    for index, lex in enumerate(sentence):
        if(index + 1 < len(sentence) and index - 1 >=0):
            if lex == "IMPLIES" and sentence[index + 1] == "NOT":
                sentence[index + 1] = "NOT "+ sentence[index + 2]
                sentence.pop(index + 2)
            elif lex == "EQUIVALENT" and sentence[index + 1] == "NOT":
                sentence[index + 1] = "NOT " + sentence[index + 2]
                sentence.pop(index + 2)
    return sentence
# -----------------------------------------------------------------------------------
#                               LOGIC OPERATION
# -----------------------------------------------------------------------------------
def logicOp(sentence):
    lexemes = getLexemes(sentence)
    lexemes.pop()           # remove ; at the end

    # counting how many ident lexemes are there
    ident = []
    for lexeme in lexemes:
        if (lexeme == 'P' and 'P' not in ident) or (lexeme == 'Q' and 'Q' not in ident) or (lexeme == 'R' and 'R' not in ident):
            ident.append(lexeme)
    numOfIdent = len(ident)

    # to be printed on terminal
    origSentence = ' '.join(lexemes)

    # the following codes will make the string of the input
    # executable by the machine



    print(lexemes)
    lexemes = groupByParen(lexemes)
    lexemes = groupByNot(lexemes)
    lexemes = changeImplies(lexemes)      # change implication format
    lexemes = changeEquivalence(lexemes)    # change equivalence format
    sentence = ' '.join(lexemes).lower().replace("true", "True").replace("false", "False")
    printCode = "print(" + sentence + ")"

    if numOfIdent == 1:
        truthsOfThree = [[0], [1]]
        print("\nP           " + origSentence)

        p = True
        for item in truthsOfThree:
            if item[0] == 1:
                p = True
            else:
                p = False

            print(p, "\t\t", end="")
            exec(printCode)

    if numOfIdent == 2:
        truthsOfThree = [[0, 0], [0, 1], [1, 0], [ 1, 1]]
        print("\nP            Q        " + origSentence)

        p = True
        q = True
        for item in truthsOfThree:
            if item[0] == 1:
                p = True
            else:
                p = False
            if item[1] == 1:
                q = True
            else:
                q = False

            print(p, "\t\t", q, "\t\t", end="")
            exec(printCode)

    if numOfIdent == 3:
        truthsOfThree = [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]]
        print("\nP            Q           R       " + origSentence)

        p = True
        q = True
        r = True
        for item in truthsOfThree:
            if item[0] == 1:
                p = True
            else:
                p = False
            if item[1] == 1:
                q = True
            else:
                q = False
            if item[2] == 1:
                r = True
            else:
                r = False

            print(p, "\t\t", q, "\t\t", r, "\t\t", end="")
            exec(printCode)



# -----------------------------------------------------------------------------------
#                               MAIN FUNCTION
# -----------------------------------------------------------------------------------
try:
    runCode = False
    while runCode == False:
        inputSentence = input("Please type \"LOGIC <source code name>\" ")
        inputSentence = inputSentence.split()
        if len(inputSentence) != 2 or inputSentence[0] != ("LOGIC" or "logic"):
            print("INVALID INPUT. Again :)")
        else:
            with open(inputSentence[-1]) as text:
                sentences = [line.rstrip('\n') for line in text]
            runCode = True
            break



    flag = True
    i = 0

    while i < len(sentences) and flag == True:
        temp = sentences[i]
        temp = temp.upper()
        print("\n" + temp)
        # check the syntax of each sentence
        if checkSyntax(temp) == False:
            flag = False
            break

        printTokens(temp)
        if checkAtomic(temp) == False:
            logicOp(temp)

        tempSentence = getLexemes(temp)
        tempSentence = changeImplies(tempSentence)

        i += 1

    text.close()

except:
    print("ERROR [File not found. Please check the file name.]")

