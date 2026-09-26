%{
#include "parser.tab.h"
#include "ast.h"
%}

%option noyywrap
%option nounput
%option noinput

%%

    /*
    [a-zA-Z] {
        yylval.c = yytext[0];
        return LETTER;
    }
    */

[,] {
    yylval.c = yytext[0];
    return SEPARATOR;
}

[\?\!\.] {
    yylval.c = yytext[0];
    return TERMINATOR;
}

[ \n\r\t]+ {
    return WHITESPACE;
}

. {
    yylval.c = yytext[0];
    return LETTER;
}

%%

