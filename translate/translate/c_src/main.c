#include "ast.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern int yyparse(void);
extern void *yy_scan_string(const char *);
extern void yy_delete_buffer(void *buffer);
extern Document *root;

int ends_with(const char *str, const char *suffix) {
    if (!str || !suffix)
        return 0;

    size_t len_str = strlen(str);
    size_t len_suf = strlen(suffix);

    if (len_suf > len_str)
        return 0;

    return strcmp(str + len_str - len_suf, suffix) == 0;
}

void replace_char(char *c) {
    switch (*c) {
    case 't':
    case 'T':
        *c -= 0x10;
        break;
    case 'k':
    case 'K':
        *c -= 0x4;
        break;
    case 'p':
    case 'P':
        *c -= 0xE;
        break;
    default:
        break;
    }
}

void adjust_word(Word *w) {
    if (ends_with(w->text, "ch")) {
        w->text[w->wordlen - 2] = '\0';
        w->wordlen -= 2;
    }
}

void double_r(Word *w) {
    if (!w)
        return;

    size_t count = 0;
    for (const char *p = w->text; *p; p++)
        if (*p == 'r')
            count++;

    if (count == 0)
        return;

    size_t old_len = strlen(w->text);
    char *src = w->text + old_len;
    char *dst = src + count;

    while (src != w->text) {
        src--;
        dst--;
        *dst = *src;
        if (*src == 'r')
            *--dst = 'r';
    }

    w->wordlen = old_len + count;
}

void switch_first_two(Sentence *s) {
    if (!s || !s->words || s->wordcount < 2)
        return;

    Word *first = s->words;
    Word *second = first->next;
    first->next = second->next;
    second->next = first;
    s->words = second;
}

__attribute__((visibility("default")))
char *translate(const char *text) {
    setvbuf(stdout, NULL, _IONBF, 0);
    if (!text)
        return NULL;

    void *buffer = yy_scan_string(text);

    if (yyparse() != 0) {
        fprintf(stderr, "Parsing failed.\n");
        yy_delete_buffer(buffer);
        return NULL;
    }
    if (!root) return strdup("");
    char_visitor(root, replace_char);
    word_visitor(root, double_r);
    word_visitor(root, adjust_word);
    sentence_visitor(root, switch_first_two);

    char *translation = build_document(root);

    free_document(root);
    root = NULL;

    yy_delete_buffer(buffer);
    return translation;
}
