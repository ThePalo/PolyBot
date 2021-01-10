grammar Expr ;

root : expr EOF ;

expr : (ASSIGNMENT | OPERATION | COMMAND) ;

ASSIGNMENT : ID ':=' OPERATION ;

COMMAND
    : PRINT ('"'WORD*'"'|OPERATION)
    | AREA OPERATION
    | PERIMETER OPERATION
    | VERTICES OPERATION
    | CENTROID OPERATION
    | COLOR ID ',' '{'VALCOLOR ' ' VALCOLOR ' ' VALCOLOR '}'
    | INSIDE ((POINT ' ' POINT) | OPERATION) ',' OPERATION
    | EQUAL OPERATION ',' OPERATION
    | DRAW OUTPUT ',' OPERATION ',' OPERATION
    ;

PRINT : 'print' ;
AREA : 'area' ;
PERIMETER : 'perimeter' ;
VERTICES : 'vertices' ;
CENTROID : 'centroid' ;
COLOR : 'color' ;
INSIDE : 'inside' ;
EQUAL : 'equal' ;
DRAW : 'draw' ;
OUTPUT : '"'WORD'"''.png' ;

OPERATION
    : '(' OPERATION ')'
    | OPERATION (INTERSECT | UNION) OPERATION
    | BOX OPERATION
    | NCREATE [0-9]+
    | ID
    | LISTPOINTS
    ;

INTERSECT : '*' ;
UNION : '+' ;
BOX : '#' ;
NCREATE : '!' ;

ID : ([a-z] | [A-Z]) ([a-z] | [A-Z] | '-' | '_' | [0-9])* ;

LISTPOINTS : '[' POINT (POINT)* ']' ;

POINT : FLOAT FLOAT ;

FLOAT : '-'? [0-9]+ '.' [0-9]*
    | '-'?'.' [0-9]+
    | '-'? [0-9]+
    ;

VALCOLOR: '1'
    | '1' '.' '0'*
    | '0' '.' [0-9]*
    | '.' [0-9]*
    | '0'
    ;

COMMENT : '//' (WORD | ID | FLOAT | ' ')* '\n' -> skip ;
WS : [ \r\n\t]+ -> skip ;
WORD : ([a-z] | [A-Z] | '-' | '_')+ ;