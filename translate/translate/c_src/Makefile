# Compiler and flags
CC = gcc
CFLAGS = -Wall -s -fvisibility=hidden -O1 -fno-omit-frame-pointer -shared -fPIC -ll
LEX = flex
YACC = bison

# Target executable
TARGET = libparser.so

# Source files
LEX_SRC = parser.l
YACC_SRC = parser.y
C_SRC = main.c ast.c

# Generated files
LEX_OUT = lex.yy.c
YACC_OUT = parser.tab.c
YACC_HDR = parser.tab.h

# Object files
OBJS = lex.yy.o parser.tab.o main.o ast.o

# Default target
all: $(TARGET)

# Build the executable
$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $(OBJS)

# Generate lexer C code
$(LEX_OUT): $(LEX_SRC) $(YACC_HDR)
	$(LEX) $(LEX_SRC)

# Generate parser C code and header
$(YACC_OUT) $(YACC_HDR): $(YACC_SRC)
	$(YACC) -d $(YACC_SRC)

# Compile generated lexer
lex.yy.o: $(LEX_OUT) ast.h $(YACC_HDR)
	$(CC) $(CFLAGS) -c $(LEX_OUT)

# Compile generated parser
parser.tab.o: $(YACC_OUT) ast.h
	$(CC) $(CFLAGS) -c $(YACC_OUT)

# Compile main.c
main.o: main.c ast.h
	$(CC) $(CFLAGS) -c main.c

# Compile ast.c
ast.o: ast.c ast.h
	$(CC) $(CFLAGS) -c ast.c

# Clean generated files
clean:
	rm -f $(OBJS) $(LEX_OUT) $(YACC_OUT) $(YACC_HDR)

# Phony targets
.PHONY: all clean
