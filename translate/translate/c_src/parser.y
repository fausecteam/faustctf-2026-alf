%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ast.h"

int yylex(void);
void yyerror(const char *s);

Document *root = NULL;
%}

%code requires {
#include "ast.h"
}

%union {
    char c;
    Word *word;
    Sentence *sentence;
    Document *document;
}

%token <c> LETTER
%token <c> TERMINATOR
%token SEPARATOR WHITESPACE

%type <word> word
%type <sentence> sentence sentence_body
%type <document> input text

%defines
%define parse.trace
%define parse.error verbose

%%

input:
    text

text:
        { $$ = NULL; }   /* empty document */
    | sentence
        {
            $$ = root = make_document($1);
        }
    | text WHITESPACE sentence
        {
            $$ = root = append_sentence($1, $3);
        }
    ;

sentence:
      sentence_body TERMINATOR
        { end_sentence($1, $2); }
    ;

sentence_body:
      word
        { $$ = make_sentence($1); }
    | sentence_body boundary word
        {
            if ($1->wordcount >= MAX_SENTENCE_WORDS) {
                yyerror("sentence exceeds MAX_SENTENCE_WORDS");
                YYERROR;
            }
            $$ = append_word($1, $3);
        }
    ;
boundary:
      WHITESPACE
    | SEPARATOR WHITESPACE
    ;

word:
      LETTER
        {
            $$ = make_word($1);
        }
    | word LETTER
        {
            if (strlen($1->text) >= MAX_WORDSIZE) {
                yyerror("word exceeds MAX_WORDSIZE");
                YYERROR;
            }
            $$ = append_char($1, $2);
        }
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Parse error: %s\n", s);
}

