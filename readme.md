# CMSC 124 Machine Problem
### Language Implementation of A Grammar of Sentences in Propositional Logic Program Documentation
Name: Fernandez, Chien Carisse P.
Section: CMSC 124 SAT
Date: 18 December 2020



#### Some notes before running the program:

 1. The program only accepts **P**, **Q**, and **R** as identifiers.
 2. If the input sentence only has **1 identifier**, the identifier to be used must be **P**, not anything else. If the input sentence has **2 identifiers**, the identifiers to be used must be **P** and **Q** only.
 3. The program only accepts the following logical operations: **NOT, OR,  AND, IMPLIES,** and  **EQUIVALENT**.

This file lists and distinctly expound the different functions and variables on the code. Using Python, the code is implemented to read *readable* files from the same directory. Users need to run the code and type the following on the terminal:

> LOGIC <filename.type>

For example, if the filename is iLoveProgramming.pl, user should type the following on the terminal:

> LOGIC iLoveProgramming.pl

### Functions
#### 1. checkAtomic(string)
This function accepts a string of sentence and checks if it is atomic or not.


#### 2. getLexemes(string)
The function accepts a *string* and returns a list of the lexemes. For example,

> input: **string = "p and q;"**
> output:  **list = [ 'p', 'and', 'q', ';' ]**

 #### 3. checkSyntax (string)
 This function checks five possible syntax error in the text input file and prints the type of error found on the specific line. Here are the syntax errors the function can catch:
 

 - **Unbalanced set of parenthesis** 
	 - Example: (P AND Q) OR NOT R);
 - **Absent semicolon**
	 - Example: P AND Q
 - **Sentence ends with a connective**
	 - Example: P OR Q IMPLIES;
 - **Sentence inside a parenthesis ends with a connective**
	 - Example: (P IMPLIES) NOT Q;
 - **Lexeme not acceptable as a valid token**
	 - Example: P AND W;
		 - 'W' is not valid lexeme for this program
- **Wrong ident used**
	-  Example: NOT R; 
	- P should be used as an identifier when there's only 1
			 

#### 4. printTokens (list)
The function accepts a list of lexemes and prints each lexeme on the terminal along with its corresponding token.
#### 5. returnParen(string) and groupByParen(list)
These functions will scan through the list of lexemes and group those that are inside a parentheses. This will make it easier to translate sentence with implication and equivalence logical operations. For example:

> input: [ 'P, 'IMPLIES, '(', 'P', 'AND', 'Q' ,')' ] 
> output: [ 'P', 'IMPLIES',  '(P AND Q)' ]

#### 6. groupByNot
This function will group those identifiers that are with negation. Through which, the translation of implication and negation sentences can be made.

> input: [ 'P', 'AND',  'NOT',  'Q' ]
> ouput: [ 'P', 'AND', 'NOT Q' ]

#### 7. changeImplies (list)
Note that:

> **p => q  ≡  ¬ p ∨ q**
>
This function translates the form **p implies q** into **not p or q** so that the program can execute the input code.
#### 8. changeEquivalence (list)
Note that:

> **p ⟷ q  ≡  (¬ p ∨ q) ∧ (¬ q ∨ p)**

This function translates the form **p equivalent q**'into **(not p or q) and (not q or p)** so that the program can execute the input code.
#### 9. logicOp(list)
This function accepts a list of lexemes then converts it into a string that's executable by the machine program. For example:

> input: **[ 'P' , 'IMPLIES' , '(NOT FALSE AND TRUE)']**
> translatedInput: "not p or not False and True"

After translating, the function will print the truth table of the input sentence.
|P| P IMPLIES (NOT FALSE AND TRUE) |
|--|--|
| False | True |
| True| True  |

-- end of document --
