#ifndef AST_H
#define AST_H

#include <stdint.h>

#define MAX_WORDSIZE 64
#define MAX_SENTENCE_WORDS 255

typedef struct Word {
    char text[MAX_WORDSIZE+1];
    struct Word *next;
    uint8_t wordlen;
} Word;

typedef struct Sentence {
    uint8_t wordcount;
    char terminator;
    Word *words;
    struct Sentence *next;
} Sentence;

typedef struct Document {
    Sentence *sentences;
} Document;

/* Word functions */
Word *make_word(char c);
Word *append_char(Word *w, char c);

/* Sentence functions */
Sentence *make_sentence(Word *w);
Sentence *append_word(Sentence *s, Word *w);
Sentence *end_sentence(Sentence *s, char c);

/* Document functions */
Document *make_document(Sentence *s);
Document *append_sentence(Document *d, Sentence *s);

/* Transformations */
void char_visitor(Document *d, void (*f)(char*));
void word_visitor(Document *d, void (*f)(Word*));
void sentence_visitor(Document *d, void (*f)(Sentence*));

/* Utility */
char *build_document(Document *d);
void debug_document(Document *d);
void free_document(Document *d);

#endif

