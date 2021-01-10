grammar Expr ;

root : expr* EOF ;

expr 
    : assignment
    | operation 
    | command
    ;

assignment : ID ':=' operation ;

command
    : printCommand
    | areaCommand 
    | perimeterCommand
    | verticesCommand
    | centroidCommand
    | colorCommand
    | insideCommand
    | equalCommand
    | drawCommand
    ;

printCommand : 'print' (string|operation) ;
areaCommand : 'area' operation ;
perimeterCommand : 'perimeter' operation ;
verticesCommand : 'vertices' operation ;
centroidCommand : 'centroid' operation ;
colorCommand : 'color' variable ',' rgbColor ;
insideCommand : 'inside' operation ',' operation ;
equalCommand : 'equal' operation ',' operation ;
drawCommand : 'draw' output ',' listOperations;


operation 
    : parenthesisOP
    | operation (INTERSECT | UNION) operation
    | boundingBoxOp
    | nCreateOp
    | variable
    | listpoints
    ;

parenthesisOP : '(' operation ')' ;
boundingBoxOp : '#' operation ;
nCreateOp : '!' real ;

INTERSECT : '*' ;
UNION : '+' ;


variable : ID ;
ID : [a-zA-Z] [a-zA-Z0-9_-]* ;

listpoints : '[' (point)* ']' ;

point : real real ;

real: FLOAT ;
FLOAT
    : '-'? [0-9]+ '.' [0-9]*
    | '-'?'.' [0-9]+
    | '-'? [0-9]+
    ;

rgbColor : '{'real real real'}' ;

listOperations: (operation ',')* operation ;

output: OUTPUT ;
OUTPUT: '"' WORD '.png' '"' ;

COMMENT : '//' ~[\r\n]* -> skip ;
WS : [ \r\n\t]+ -> skip ;
WORD : [a-zA-Z_-]+ ;
string : STRING ;
STRING : '"'(~'"')*'"' ;
