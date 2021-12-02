grammar BKOOL;

@lexer::header {
from lexererr import *
}

options{
	language=Python3;
}

program: classdecl+ EOF;
classdecl
	: CLASS ID EXTENDS ID LP memberlist RP
	| CLASS ID LP memberlist RP
	;
memberlist
	: attribute memberlist
	| method memberlist
	|
	;

// Attribute declaration
attribute
	: FINAL STATIC typekeyword initials SEMI
	| STATIC storedecl
	| storedecl
	;
storedecl: vardecl | constdecl;
vardecl: typekeyword initials SEMI;
constdecl: FINAL typekeyword initials SEMI;
initials
	: ID (INIT exp)? COMMA initials
	| ID (INIT exp)?
	;

// Method declaration
method
	: STATIC typekeyword ID LB paramlist RB blockstatement
	| STATIC typekeyword ID LB RB blockstatement
	| STATIC VOIDTYPE ID LB paramlist RB blockstatement
	| STATIC VOIDTYPE ID LB RB blockstatement
	| typekeyword ID LB paramlist RB blockstatement
	| typekeyword ID LB RB blockstatement
	| VOIDTYPE ID LB paramlist RB blockstatement
	| VOIDTYPE ID LB RB blockstatement
	| ID LB paramlist RB blockstatement
	| ID LB RB blockstatement
	;
paramlist
	: paramdecl SEMI paramlist
	| paramdecl
	;
paramdecl: typekeyword idlist;
idlist
	: ID COMMA idlist
	| ID
	;
typekeyword
	: BOOLEANTYPE
	| INTTYPE
	| FLOATTYPE
	| STRINGTYPE
	| ID // class type
	| arraytype // array type
	;
arraytype
	: BOOLEANTYPE LS INTLIT RS
	| INTTYPE LS INTLIT RS
	| FLOATTYPE LS INTLIT RS
	| STRINGTYPE LS INTLIT RS
	| ID LS INTLIT RS
	;

// Statement: blockstatement, assignment, ...
statement
	: assignment
	| breakstmt
	| continuestmt
	| ret
	| callstmt
	| ifstmt
	| forstmt
	| blockstatement
	;

assignment: lhs ASSIGN exp SEMI;
lhs
	: ID
	| exparray
	| fieldaccess
	;
fieldaccess: exp DOT ID;
ifstmt
	: IF exp THEN statement
	| IF exp THEN statement ELSE statement
	;

forstmt
	: FOR ID ASSIGN exp TO exp DO statement
	| FOR ID ASSIGN exp DOWNTO exp DO statement
	;

blockstatement: LP storedecls statements RP;
storedecls
	: storedecl storedecls
	|
	;
statements
	: statement statements
	|
	;

callstmt
	: expcall DOT ID LB arglist RB SEMI
	| expcall DOT ID LB RB SEMI
	;
arglist
	: exp COMMA arglist
	| exp
	;

continuestmt: CONTINUE SEMI;
breakstmt: BREAK SEMI;
ret: RETURN exp SEMI;

// Expression
exp
	: expnoneay GT expnoneay
	| expnoneay LT expnoneay
	| expnoneay GTOE expnoneay
	| expnoneay LTOE expnoneay
	| expnoneay
	;
expnoneay
	: explogic EQUAL explogic
	| explogic NOTEQUAL explogic
	| explogic
	;
explogic
	: explogic AND exp1
	| explogic OR exp1
	| exp1
	;
exp1
	: exp1 ADD exp2
	| exp1 SUB exp2
	| exp2
	;
exp2
	: exp2 MUL expstring
	| exp2 DIVFLOAT expstring
	| exp2 DIVINT expstring
	| exp2 MOD expstring
	| expstring
	;
expstring
	: expstring CONCAT expnot
	| expnot
	;
expnot
	: NOT expnot
	| expsign
	;
expsign
	: ADD expsign
	| SUB expsign
	| exparray
	;
exparray
	: expcall LS exp RS
	| expcall
	;
expcall
	: expcall DOT ID LB arglist RB
	| expcall DOT ID LB RB
	| expcall DOT ID
	| expnew
	;
expnew
	: NEW ID LB arglist RB
	| NEW ID LB RB
	| LB exp RB
	| term
	;
term
	: INTLIT
	| FLOATLIT
	| TRUE
	| FALSE
	| STRINGLITS
	| LP arraylits RP
	| NIL
	| THIS
	| ID;

arraylits
	: arrayelelits COMMA arraylits
	| arrayelelits
	;
arrayelelits
	: INTLIT
	| FLOATLIT
	| TRUE
	| FALSE
	| STRINGLITS
	;
// arrayintlits
// 	: INTLIT COMMA arrayintlits
// 	| INTLIT
// 	;
// arrayfloatlits
// 	: FLOATLIT COMMA arrayfloatlits
// 	| FLOATLIT
// 	;
// arraybooleanlits
// 	: TRUE COMMA arraybooleanlits
// 	| FALSE COMMA arraybooleanlits
// 	| TRUE
// 	| FALSE
// 	;
// arraystringlits
// 	: STRINGLITS COMMA arraystringlits
// 	| STRINGLITS
// 	;

////////////////////LEXER///////////////////////////////

INLINECOMMENT: '#' (~[\n\r])* -> skip;
// bắt lỗi ko có */ để kết thúc cmt??
BLOCKCOMMENT: '/*' .*? '*/' -> skip;

INTTYPE: 'int' ;

VOIDTYPE: 'void'  ;

// for keywords
BOOLEANTYPE: 'boolean';
BREAK: 'break';
CLASS: 'class';
CONTINUE: 'continue';
DO: 'do';
ELSE: 'else';
EXTENDS: 'extends';
FLOATTYPE: 'float';
IF: 'if';
NEW: 'new';
STRINGTYPE: 'string';
THEN: 'then';
FOR: 'for';
RETURN: 'return';
TRUE: 'true';
FALSE: 'false';
NIL: 'nil';
THIS: 'this';
FINAL: 'final';
STATIC: 'static';
TO: 'to';
DOWNTO: 'downto';

// for operators
// [+\-*/\\%<>!^](10) new
INIT: '=';
ADD: '+';
SUB: '-';
MUL: '*';
DIVFLOAT: '/';
DIVINT: '\\';
MOD: '%';
AND: '&&';
OR: '||';
NOT: '!';
EQUAL: '==';
NOTEQUAL: '!=';
GT: '>';
LT: '<';
GTOE: '>=';
LTOE: '<=';
CONCAT: '^';
ASSIGN: ':=';

// identifier
ID: [a-zA-Z_] [a-zA-Z_0-9]*;

// literals
INTLIT: [0-9]+;
fragment EXPONENT: [eE] [+-]? [0-9]+;
fragment DECIMAL: '.' [0-9]* EXPONENT?;
FLOATLIT: [0-9]+ (EXPONENT DECIMAL? | DECIMAL);


ILLEGAL_ESCAPE: '"' (~["\\\n\r] | '\\' [bfrnt"\\])* '\\' (~[bfrnt"\\]) {raise IllegalEscape(self.text)};
UNCLOSE_STRING: '"' (~["\\\n\r] | '\\' [bfrnt"\\])* {raise UncloseString(self.text)};
STRINGLITS: '"' (~["\\\n\r] | '\\' [bfrnt"\\])* '"';


// Seperators:
LS: '[';
RS: ']';
LB: '(' ;
RB: ')' ;
LP: '{';
RP: '}';
SEMI: ';';
COLON: ':';
DOT: '.';
COMMA: ',';

WS : [ \f\t\r\n]+ -> skip ; // skip spaces, tabs, newlines


ERROR_CHAR: . {raise ErrorToken(self.text)};