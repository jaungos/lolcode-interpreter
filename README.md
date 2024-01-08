# LOLCODE Interpreter in Python

## About
The program is a LOLCODE interpreter written in Python. It uses an object-oriented approach and takes advantage of recursive function calls. LOLCODE's homepage is at lolcode.org.

<div align = "center">

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![LOLCODE](https://img.shields.io/badge/_-LOL-CC9900.svg?style=for-the-badge)

</div>

## Installing Dependencies 
* For Windows, it should be run in a cmd terminal
```bash
py -m venv env
env/Scripts/activate # Open a new cmd terminal in the same directory

pip install tk
pip install ttkthemes
```

## Running
Open a terminal at the sourcecode folder and run the command: 
### Linux
```bash
python3 main.py
```
### Windows 
* It should be run in the cmd terminal
```bash
py main.py 
```

## Project Specifications (LOLCODE v1.2)
### WHITESPACES
One line per statement only. Each statement must be delimited by new lines. Only one whitespace between keywords is supported. Spaces inside YARN literals are respected and maintained. 

### COMMENTS
Comments are ignored. The keywords OBTW and TLDR must have their own lines. 

### VARIABLES
All variables are declared after a WAZZUP. Variables names must start with a letter, with the rest being any combitaion of letters, numbers, and/or underscores. Spaces, dashes, and other special symbols are not supported.
#### Variable Declaration
Each declaration is done using the keyword I HAS A
#### Variable Initialization (optional)
- Initialization is done using the keyword ITZ
- Possible values are literals, the value of another variable, or a result of an expression.
- Initialization may contain any operation that results to a literal value.

### DATA TYPES
Variables are dynamically-typed

| DATA TYPE | IN LOLCode | DESCRIPTION |
| --- | --- | --- |
| untyped | NOOB | The data type of uninitialized variables is NOOB. |
| integer | NUMBR | These are sequences of digits without a decimal point (.) and are not enclosed by double quotes. Negative numbers must be preceded by a negative sign (-), but positive numbers MUST NOT be preceded by a positive sign (+). |
| float | NUMBAR | They are sequences of digits with exactly one decimal point (.) and are not enclosed by double quotes. They may be preceded by a negative sign (-) to indicate that the value is negative. For positive values, it MUST NOT be preceded by a positive sign (+) to indicate that it is positive. |
| string | YARN | These are delimited by double quotes (“”). |
| boolean | TROOF | The value of a TROOF can be WIN (true) or FAIL (false). |

### OPERATIONS
Operations are in prefix notation. The AN keyword is required to separate operands.
#### Unary Operations (can be nested)
- NOT
#### Binary Operations (can be nested)
All operations except:
- SMOOSH
- ALL OF
- ANY OF
#### Infinite Arity Operations (cannot be nested)
- SMOOSH
- ALL OF
- ANY OF
#### Input/Output
- Printing to the terminal is done using the VISIBLE keyword.
- VISIBLE has infinite arity and concatenates all of its operands after casting them to YARNs. Each operand is
separated by a ‘+’ symbol.
- The VISIBLE statement automatically adds a new line after all the arguments are printed.
- Accepting input is done using the GIMMEH keyword.
- GIMMEH must always use a variable, where the user input will be placed. The input value is always a YARN.
#### Arithmetic Operations
Mathematical operations are performed with NUMBRs and/or NUMBARs involved.
- If a value is not a NUMBAR and is not a NUMBR, it must be implicitly typecast into a NUMBAR/NUMBR depending on
the value. 
- If a value cannot be typecast, the operation must fail with an error.
- If both operands evaluate to a NUMBR, the result of the operation is a NUMBR.
- If at least one operand is a NUMBAR, the result of the operation is a NUMBAR.
- Nesting of operations is allowed, but all operations are still binary.
#### Concatenation
SMOOSH does not require the MKAY keyword.
- If the operand evaluates to another data type, they are implicitly typecast to YARNs when given to SMOOSH
#### Boolean Operations
Below are the boolean operations:
```
BOTH OF <x> AN <y> BTW and
EITHER OF <x> AN <y> BTW or
WON OF <x> AN <y> BTW xor
NOT <x> BTW not
ALL OF <x> AN <y> ... MKAY BTW infinite arity AND
ANY OF <x> AN <y> ... MKAY BTW infinite arity OR
```
- If the operands are not TROOFs, they should be implicitly typecast
- ALL OF and ANY OF cannot be nested into each other and themselves, but may have other boolean operations
as operands

```
ALL OF NOT x AN BOTH OF y AN z AN EITHER OF x AN y MKAY
BTW (!x) ⋀ (y⋀z) ⋀ (x⋁y) ← YAASSS ALLOWED!!
ALL OF ALL OF x AN y MKAY AN z MKAY BTW :( ← NOT ALLOWED!!
```
#### Typecasting
Rules for data types:
##### NOOB
- NOOBs can be implicitly typecast into TROOF. Implicit typecasting to any other type except TROOF will result in an error.
- Explicit typecasting of NOOBs is allowed and results to empty/zero values depending on the type.
##### TROOF
- The empty string (“”) and numerical zero values are cast to FAIL.
- All other values are cast to WIN.
- Casting WIN to a numerical type results in 1 or 1.0.
- Casting FAIL results in a numerical zero.
##### NUMBAR
- Casting NUMBARs to NUMBR will truncate the decimal portion of the NUMBAR.
- Casting NUMBARs to YARN will truncate the decimal portion up to two decimal
places.
##### NUMBR
- Casting NUMBRs to NUMBAR will just convert the value into a floating point. The value should be retained.
- Casting NUMBRs to YARN will just convert the value into a string of characters.
##### YARN
- A YARN can be successfully cast into a NUMBAR or NUMBR if the YARN does not contain any non-numerical, non-hyphen, non-period characters.

Explicit typecasting a value can be done using the MAEK operator. This operator, however, only modifies the
resulting value, and not the variable involved, if there is any.
```
I HAS A var1 ITZ 12 BTW var1 is a NUMBR
MAEK var1 A NUMBAR BTW returns NUMBAR equivalent of var1 to IT (12.0)
BTW var1 is still a NUMBR
MAEK var1 YARN BTW returns YARN equivalent of var1 to IT (“12”)
BTW var1 is still a NUMBR
```
Re-casting a variable can be done via normal assignment statement involving MAEK or via IS NOW A.
```
I HAS A number ITZ 17 BTW number is NUMBR type
number IS NOW A NUMBAR BTW number is NUMBAR type now (17.0)
number R MAEK number YARN BTW number reassigned to the YARN value of number (“17.0”)
```

### STATEMENTS
#### Expression Statements
The result of an expression may not be assigned to a variable. In this case, its result will be stored in the implicit variable IT.

#### Assignment Statements
- The assignment operation keyword is R.
- The left-hand side is always a receiving variable, while the right side may be a literal, variable, or an
expression.
```
<variable> R <literal>
<variable> R <variable>
<variable> R <expression>
```
#### Flow-control Statements
##### If-then Statements
Uses five keywords: O RLY?, YA RLY, MEBBE, NO WAI, and OIC. The syntax for if-then statements is:
```
<expression> BTW result is stored in IT
O RLY?
YA RLY BTW if
<if code block>
NO WAI BTW else
<else code block>
OIC
``` 
- Indentation is irrelevant.
- If the IT variable can be cast to WIN, the if-clause executes. Otherwise, the else-clause executes.
- Implementing MEBBE (else-if) clauses is not required.
- The if-clause starts at the YA RLY keyword and ends when the NO WAI or OIC keyword is encountered.
- The else-clause starts at the NO WAI keyword and ends when the OIC keyword is encountered.
- You may assume that O RLY?, YA RLY, NO WAI, and OIC are alone in their respective lines. MEBBE, if implemented, should be followed by an expression in the same line.

#### Switch-case Statements 
Uses four keywords keywords used in a switch-case in LOLCode: WTF?, OMG, OMGWTF, and OIC. The syntax for switch-case statements is shown below:
```
WTF? BTW uses value in IT
OMG <value literal>
<code block>
[OMG <value literal>
<code block>...]
[OMGWTF
<code block>]
OIC
```
- Once WTF? is encountered, the value of the implicit IT variable is compared to each case, denoted by an OMG keyword. If IT and the case are equal, the succeeding code block executes until a GTFO (break) or an OIC keyword is encountered.
- The cases may be of any literal type (NUMBRs, NUMBARs, YARNs, and TROOFs).
- The default case is specified by OMGWTF and is executed if none of the preceding cases match the value of IT. Execution then stops when an OIC is encountered.

#### Loops
Follows the form:
```
IM IN YR <label> <operation> YR <variable> [TIL|WILE <expression>]
<code block>
IM OUTTA YR <label>
```
- The IM IN YR <label> and IM OUTTA YR <label> clauses specify the start and end of the loop. The <label> follows the format for a valid variable name, and is used as a delimiter, especially in the case where nested loops are implemented.
- The <operation> can either be UPPIN (increment by 1) or NERFIN (decrement by 1), which modifies the <variable> that follows.
- The variable specified in <variable> should be an existing variable (i.e., declared) and whose value can
be cast to a numerical value so it can be processed by UPPIN/NERFIN.
- The loops can be terminated by meeting the condition expressions TIL/WILE or by issuing a GTFO statement inside the loop.
- The TIL <expression> clause will repeat the loop as long as <expression> is FAIL.
- The WILE <expression> clause will repeat the loop as long as <expression> returns WIN.
```
I HAS A temp ITZ 2
BTW prints 2 to 9 using TIL
IM IN YR print10 UPPIN YR temp TIL BOTH SAEM temp AN 10
VISIBLE temp
IM OUTTA YR print10
BTW at this point, temp’s value is 10, so we must reassign its initial value
temp R 2
BTW prints 2 to 9 but using WILE
IM IN YR print10 UPPIN YR temp WILE DIFFRINT temp AN 10
VISIBLE temp
IM OUTTA YR print10
```

### FUNCTIONS
#### Definition
Functions have a fixed number of parameters in the definition.
```
HOW IZ I <function name> [YR <parameter1> [AN YR <parameter2> [AN YR <parameter3> ...]]]
BTW function body
IF U SAY SO
```
- <parameter1>, <parameter2>, and <parameter3> are the parameters of the function. If there are no
parameters, then the parameters will be ommitted:
```
HOW IZ I sample_function BTW function with 0 arguments
HOW IZ I sample_function2 YR x AN YR y BTW function with 2 arguments
```
- Functions cannot access identifiers outside of it. Only the arguments passed are accessible to the function.
- Arguments are passed via pass-by value only.
- The parameters in the function become a variable of that function, with the passed argument as the initial value.

#### Returning
- FOUND YR <expression> returns the value of the expression.
- GTFO returns with no value (NOOB), but if no GTFO is found, the return type will also be NOOB automatically.
- Return values will automatically be stored in the implicit variable IT.
#### Calling
Functions can be called using the following syntax:
```
I IZ <function name> [YR <expression1> [AN YR <expression2> AN YR <expression2>]] MKAY
```
Expressions must be executed first before executing the function body.
