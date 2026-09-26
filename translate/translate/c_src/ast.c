#include "ast.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* ---------------- Word ---------------- */
Word *make_word(char c) {
    Word *w = malloc(sizeof(Word));
    if (!w)
        return NULL;
    w->text[0] = c;
    w->text[1] = '\0';
    w->next = NULL;
    w->wordlen = 1;
    return w;
}

Word *append_char(Word *w, char c) {
    w->text[w->wordlen++] = c;
    w->text[w->wordlen] = '\0';
    return w;
}

/* ---------------- Sentence ---------------- */
Sentence *make_sentence(Word *w) {
    Sentence *s = malloc(sizeof(Sentence));
    if (!s)
        return NULL;
    s->words = w;
    s->next = NULL;
    s->wordcount = 1;
    return s;
}

Sentence *append_word(Sentence *s, Word *w) {
    Word *cur = s->words;
    while (cur->next)
        cur = cur->next;
    cur->next = w;
    s->wordcount++;
    return s;
}

Sentence *end_sentence(Sentence *s, char c) {
    s->terminator = c;
    return s;
}

/* ---------------- Document ---------------- */
Document *make_document(Sentence *s) {
    Document *d = malloc(sizeof(Document));
    if (!d)
        return NULL;
    d->sentences = s;
    return d;
}

Document *append_sentence(Document *d, Sentence *s) {
    Sentence *cur = d->sentences;
    while (cur->next)
        cur = cur->next;
    cur->next = s;
    return d;
}

/* ------------- Transformations ------------- */
void char_visitor(Document *d, void (*f)(char *)) {
    uint8_t i = 0;
    uint8_t j = 0;
    for (Sentence *s = d->sentences; s; s = s->next) {
        i = 0;
        Word *w = s->words;
        do {
            for (j = 0; j < w->wordlen; j++) {
                f(&w->text[j]);
            }
            i++;
            w = w->next;
        } while (i < s->wordcount);
    }
}

void word_visitor(Document *d, void (*f)(Word *)) {
    uint8_t i = 0;
    for (Sentence *s = d->sentences; s; s = s->next) {
        i = 0;
        Word *w = s->words;
        do {
            f(w);
            i++;
            w = w->next;
        } while (i < s->wordcount);
    }
}

void sentence_visitor(Document *d, void (*f)(Sentence *)) {
    for (Sentence *s = d->sentences; s; s = s->next) {
        f(s);
    }
}

/* ---------------- Utilities ---------------- */
char *build_document(Document *d) {
    if (!d)
        return NULL;

    size_t cap = 128, used = 0;
    char *doc = malloc(cap);
    if (!doc)
        return NULL;

    for (Sentence *s = d->sentences; s; s = s->next) {
        uint8_t i = 0;
        Word *w = s->words;
        do {
            size_t needed = used + 1 + w->wordlen + 2;
            if (needed > cap) {
              cap *= 2;
              char *tmp = realloc(doc, cap);
              if (!tmp) {
                free(doc);
                return NULL;
              }
              doc = tmp;
            }
            used += sprintf(doc + used, "%s%s", (used == 0) ? "" : " ", w->text);
            i++;
            w = w->next;
        } while (i < s->wordcount);
        used += sprintf(doc + used, "%c", s->terminator);

    }
    return doc;
}

void free_document(Document *d) {
    if (d == NULL)
        return;

    Sentence *s = d->sentences;
    while (s) {
        uint8_t i = 0;
        Word *w = s->words;
        do {
            Word *wn = w->next;
            free(w);
            i++;
            w = wn;
        } while (i < s->wordcount-1);
        Sentence *sn = s->next;
        free(s);
        s = sn;
    }
    free(d);
}
