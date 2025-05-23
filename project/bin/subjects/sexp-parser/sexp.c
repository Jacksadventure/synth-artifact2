#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Wunused-label"
#ifdef __APPLE__
    #include "fmemopen/fmemopen.h"
#endif

int my_fgetc(FILE* stream) {
    int c = fgetc(stream);
    char b = c;
    return c;
}


/*
 * bool
 */

typedef unsigned char bool;

enum {
    true  = 1,
    false = 0
};


/*
 * sexp
 */

enum {
  TYPE_NIL     = 1,
  TYPE_SYMBOL  = 2,
  TYPE_STRING  = 3,
  TYPE_INTEGER = 4,
  TYPE_PAIR    = 5
};

typedef struct {
    unsigned char tt;
} sexp_t;

void destroy_sexp(sexp_t *);

void print_sexp(sexp_t *);


/*
 * symbol
 */

typedef struct {
    unsigned char tt;
    const char *name;
} symbol_t;

bool is_symbol(sexp_t *sexp)
{
    return sexp->tt == TYPE_SYMBOL;
}

const char *symbol_name(symbol_t *symbol)
{
    return symbol->name;
}

sexp_t *create_symbol(const char *name)
{
    symbol_t *symbol = (symbol_t *)malloc(sizeof(symbol_t));
    if (!symbol) exit(-1);

    symbol->tt = TYPE_SYMBOL;
    symbol->name = strdup(name);

    return (sexp_t *)symbol;
}

void destroy_symbol(symbol_t *symbol)
{
    free((char *)symbol->name);
    free(symbol);
}

void print_symbol(symbol_t *symbol)
{
    printf("%s", symbol->name);
}


/*
 * string
 */

typedef struct {
    unsigned char tt;
    const char *str;
} string_t;

bool is_string(sexp_t *sexp)
{
    return sexp->tt == TYPE_STRING;
}

const char *string_str(string_t *string)
{
    return string->str;
}

sexp_t *create_string(const char *str)
{
    string_t *string = (string_t *)malloc(sizeof(string_t));
    if (!string) exit(-1);

    string->tt = TYPE_STRING;
    string->str = strdup(str);

    return (sexp_t *)string;
}


void destroy_string(string_t *string)
{
    free((char *)string->str);
    free(string);
}

void print_string(string_t *string)
{
    printf("\"%s\"", string->str);
}


/*
 * integer
 */

typedef struct {
    unsigned char tt;
    int value;
} integer_t;

bool is_integer(sexp_t *sexp)
{
    return sexp->tt == TYPE_INTEGER;
}

int integer_value(integer_t *integer)
{
    return integer->value;
}

sexp_t *create_integer(const int value)
{
    integer_t *integer = (integer_t *)malloc(sizeof(integer_t));
    if (!integer) exit(-1);

    integer->tt = TYPE_INTEGER;
    integer->value = value;

    return (sexp_t *)integer;
}

void destroy_integer(integer_t *integer)
{
    free(integer);
}

void print_integer(integer_t *integer)
{
    printf("%d", integer->value);
}


/*
 * nil
 */

typedef struct {
    unsigned char tt;
} nil_t;

bool is_nil(sexp_t *sexp)
{
    return sexp->tt == TYPE_NIL;
}

sexp_t *create_nil()
{
    nil_t *nil = (nil_t *)malloc(sizeof(nil_t));
    if (!nil) exit(-1);

    nil->tt = TYPE_NIL;

    return (sexp_t *)nil;
}

void destroy_nil(nil_t *nil)
{
    free(nil);
}

void print_nil(nil_t *nil)
{
    printf("()");
}


/*
 * pair
 */

typedef struct {
    unsigned char tt;
    sexp_t *car;
    sexp_t *cdr;
} pair_t;

bool is_pair(sexp_t *sexp)
{
    return sexp->tt == TYPE_PAIR;
}

sexp_t *pair_car(pair_t *pair)
{
    return pair->car;
}

sexp_t *pair_cdr(pair_t *pair)
{
    return pair->cdr;
}

sexp_t *create_pair(sexp_t *car, sexp_t *cdr)
{
    pair_t *pair = (pair_t *)malloc(sizeof(pair_t));
    if (!pair) exit(-1);

    pair->tt = TYPE_PAIR;
    pair->car = car;
    pair->cdr = cdr;

    return (sexp_t *)pair;
}

void destroy_pair(pair_t *pair)
{
    destroy_sexp(pair->car);
    destroy_sexp(pair->cdr);
    free(pair);
}

void print_pair(pair_t *pair)
{
    printf("(");
begin:
    print_sexp(pair->car);
    if (is_nil(pair->cdr)) {
        printf(")");
    } else if (is_pair(pair->cdr)) {
        printf(" ");
        pair = (pair_t *)pair->cdr;
        goto begin;
    } else {
        printf(" . ");
        print_sexp(pair->cdr);
        printf(")");
    }
}


/*
 * sexp - continued
 */

void destroy_sexp(sexp_t *sexp)
{
    switch (sexp->tt) {
    case TYPE_NIL:
        destroy_nil((nil_t *)sexp);
        return;
    case TYPE_SYMBOL:
        destroy_symbol((symbol_t *)sexp);
        return;
    case TYPE_STRING:
        destroy_string((string_t *)sexp);
        return;
    case TYPE_INTEGER:
        destroy_integer((integer_t *)sexp);
        return;
    case TYPE_PAIR:
        destroy_pair((pair_t *)sexp);
        return;
    default:
        fprintf(stderr, "Invalid S-expression.\n");
        exit(-1);
    }
}

void print_sexp(sexp_t *sexp)
{
    switch (sexp->tt) {
    case TYPE_NIL:
        print_nil((nil_t *)sexp);
        return;
    case TYPE_SYMBOL:
        print_symbol((symbol_t *)sexp);
        return;
    case TYPE_STRING:
        print_string((string_t *)sexp);
        return;
    case TYPE_INTEGER:
        print_integer((integer_t *)sexp);
        return;
    case TYPE_PAIR:
        print_pair((pair_t *)sexp);
        return;
    default:
        fprintf(stderr, "Invalid S-expression.\n");
        exit(-1);
    }
}


/*
 * read
 */

bool is_invalid_character(char c)
{
    return false;
}

bool is_whitespace(char c)
{
    return c == '\t' || c == '\n' || c == '\r' || c == ' ';
}

bool is_terminating(char c)
{
    return c == '"' || c == '\'' || c == '(' || c == ')'
        || c == ',' || c == ';'  || c == '`';
}

bool is_non_terminating(char c)
{
    return c == '#';
}

bool is_macro_character(char c)
{
    return is_terminating(c) || is_non_terminating(c);
}

bool is_single_escape(char c)
{
    return c == '\\';
}

bool is_multi_escape(char c)
{
    return c == '|';
}

void nreverse(sexp_t **psexp)
{
    sexp_t *prev = create_nil();
    sexp_t *current = *psexp;
    sexp_t *next;

    while(!is_nil(current)) {
        if (!is_pair(current)) {
            fprintf(stderr, "Not list.");
            exit(-1);
        }
        next = ((pair_t *)current)->cdr;
        ((pair_t *)current)->cdr = prev;
        prev = current;
        current = next;
    }
    destroy_sexp(current);
    *psexp = prev;
}

#define EXIT_INCORRECT (1)
#define EXIT_INCOMPLETE (-1)

#define INCORRECT(_msg) { \
        fprintf(stderr, "%s\n", _msg);\
        exit(EXIT_INCORRECT); \
    }
#define INCOMPLETE(_msg) { \
        fprintf(stderr, "%s\n", _msg);\
        exit(EXIT_INCOMPLETE); \
    }

#define END_OF_FILE         INCOMPLETE("End of file.")
#define NOT_IMPLEMENTED     INCORRECT("Feature not implemented.")
#define NOT_IMPLEMENTED_(x) INCORRECT("Feature not implemented: " x)
#define READER_ERROR        INCORRECT("Reader error.")
#define UNMATCHED_CLOSE_PARENTHESIS INCORRECT("Unmatched close parenthesis.")
#define MUST_NOT_BE_REACHED INCORRECT("Must not be reached.")

sexp_t *read(FILE *, bool);

int my_EOF = EOF;


sexp_t *read_string(FILE *fp, int c)
{
#define ADD_BUF(_buf, _i, _c) do { \
        _buf[_i++] = _c; \
        if (_i == 256) { \
            fprintf(stderr, "Too long string: %s...\n", _buf); \
            exit(-1); \
        } \
    } while(0)

    char buf[256] = {0};
    int i = 0;

    while ((c = my_fgetc(fp)) != my_EOF) {

        if (is_single_escape(c)) {
            if ((c = my_fgetc(fp)) == my_EOF)
                END_OF_FILE;
            ADD_BUF(buf, i, c);
            continue;
        }

        if (c == '"')
            return create_string(buf);

        ADD_BUF(buf, i, c);
    }

    END_OF_FILE;

#undef ADD_BUF
}

sexp_t *read_list(FILE *fp, char c)
{
    sexp_t *list = create_nil();

    while ((c = my_fgetc(fp)) != my_EOF) {

        if (is_whitespace(c))
            continue;

        if (c == ')') {
            nreverse(&list);
            return list;
        }

        if (c == '.')
            NOT_IMPLEMENTED_("Dot in list");

        ungetc(c, fp);
        list = create_pair(read(fp, false), list);
    }

    END_OF_FILE;
}

bool integer(int *result, const char *str)
{
    int i = 0;
    int sign = 1;
    *result = 0; // Initialize result to 0

    if (str[i] == '+')
        i++;
    else if (str[i] == '-') { // Use 'else if' to handle '-' correctly
        sign = -1;
        i++;
    }
    if ('0' <= str[i] && str[i] <= '9') {
        *result += str[i] - '0';
        i++;
    } else
        return false;
    begin:
        if ('0' <= str[i] && str[i] <= '9') {
            *result *= 10;
            *result += str[i] - '0';
            i++;
            goto begin;
        } else if (str[i] == '\0') {
            *result *= sign; // Apply the sign here
            return true;
        } else
            return false;
}

sexp_t *read(FILE *fp, bool inRoot)
{
#define ADD_BUF(_buf, _i, _c) do { \
        _buf[_i++] = _c; \
        if (_i == 256) { \
            fprintf(stderr, "Too long symbol: %s...\n", _buf); \
            exit(-1); \
        } \
    } while(0)

    char buf[256] = {0};
    int i = 0;
    char c;
    int int_value = 0;

step1:
    if ((c = my_fgetc(fp)) == my_EOF) {
        if (inRoot) {
            return NULL;
        } else {
            END_OF_FILE; // TODO accept empty files?
        }
    }

step2:
    if (is_invalid_character(c))
        READER_ERROR;

step3:
    if (is_whitespace(c))
        goto step1;

step4:
    if (is_macro_character(c)) {

        if (c == '"') {
            sexp_t *string_sexp = read_string(fp, c);
            if (inRoot) {
                while ((c = my_fgetc(fp)) != my_EOF) {
                    if (!is_whitespace(c)) {
                        INCORRECT("Extra tokens after root S-expression.");
                    }
                }
            }
            return string_sexp;
        }

        if (c == '#')
            NOT_IMPLEMENTED_("Single Hash");

        if (c == '\'')
            NOT_IMPLEMENTED_("Single Tick");

        if (c == '(') {
            sexp_t *list = read_list(fp, c);
            if (inRoot) {
                while ((c = my_fgetc(fp)) != my_EOF) {
                    if (!is_whitespace(c)) {
                        MUST_NOT_BE_REACHED;
                    }
                }
            }
            return list;
        }

        if (c == ')')
            UNMATCHED_CLOSE_PARENTHESIS;

        if (c == ',')
            NOT_IMPLEMENTED_("Comma");

        if (c == ';')
            NOT_IMPLEMENTED_("Line Comments");

        if (c == '|')
            NOT_IMPLEMENTED_("Pipe");

        MUST_NOT_BE_REACHED;
    }

step5:
    if (is_single_escape(c)) {
        if ((c = my_fgetc(fp)) == my_EOF)
            END_OF_FILE;
        ADD_BUF(buf, i, c);
        goto step8;
    }

step6:
    if (is_multi_escape(c))
        NOT_IMPLEMENTED_("Multi Escape");

step7:
    // constituent
    ADD_BUF(buf, i, c);
    goto step8;

step8:
    if ((c = my_fgetc(fp)) == my_EOF)
        goto step10;

    if (is_non_terminating(c)) {
        ADD_BUF(buf, i, c);
        goto step8;
    }

    if (is_single_escape(c)) {
        if ((c = my_fgetc(fp)) == my_EOF)
            END_OF_FILE;
        ADD_BUF(buf, i, c);
        goto step8;
    }

    if (is_multi_escape(c))
        NOT_IMPLEMENTED_("Multi-Escape");

    if (is_invalid_character(c))
        READER_ERROR;

    if (is_terminating(c)) {
        ungetc(c, fp);
        goto step10;
    }

    if (is_whitespace(c))
        goto step10;

    // constituent
    ADD_BUF(buf, i, c);
    goto step8;

step9:
    NOT_IMPLEMENTED_("Step 9");

step10:
    if (integer(&int_value, buf)) {
        if (inRoot) {
            while ((c = my_fgetc(fp)) != my_EOF) {
                if (!is_whitespace(c)) {
                    MUST_NOT_BE_REACHED;
                }
            }
        }
        return create_integer(int_value);
    }

    if (inRoot) {
        while ((c = my_fgetc(fp)) != my_EOF) {
            if (!is_whitespace(c)) {
                MUST_NOT_BE_REACHED;
            }
        }
    }

    return create_symbol(buf);

#undef ADD_BUF
}

// Added the infrastructure from our modified cJSON version:
FILE* v = 0;

int main(int argc, char** argv) {
    if (argc > 1) {
      v = fopen(argv[1], "r");
    } else {
      v = stdin;
    }

    bool hasReadSexp = false;
    sexp_t * sexp = NULL;

    while (!hasReadSexp || sexp != NULL){
        sexp = read(v, true);
        if (sexp == NULL){
            if (!hasReadSexp){
                END_OF_FILE;
            }
            continue;
        } else {
            print_sexp(sexp);
            printf("\n");
            hasReadSexp = true;
            destroy_sexp(sexp);
            sexp = NULL;
        }
    }

    sexp = NULL;

    fclose(v);

    return 0;

}


#undef MUST_NOT_BE_REACHED
#undef UNMATCHED_CLOSE_PARENTHESIS
#undef READER_ERROR
#undef NOT_IMPLEMENTED
#undef END_OF_FILE
#undef ERROR

#pragma clang diagnostic pop

