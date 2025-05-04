// main.cpp
#include <iostream>
#include <fstream>
#include "antlr4-runtime.h"
#include "DOTLexer.h"
#include "DOTParser.h"
#include "ErrorListener.h"

int main(int argc, const char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <file.dot>\n";
        return 2;
    }

    std::ifstream in(argv[1]);
    if (!in) { perror("open"); return 2; }

    antlr4::ANTLRInputStream input(in);
    DOTLexer lexer(&input);
    antlr4::CommonTokenStream tokens(&lexer);
    DOTParser parser(&tokens);

    ExitCodeErrorListener listener;
    lexer.removeErrorListeners();
    parser.removeErrorListeners();
    lexer.addErrorListener(&listener);
    parser.addErrorListener(&listener);

    parser.graph();                       // 起始规则

    if (listener.syntaxErrorSeen)
        return listener.eofOffending ? 255 : 1;

    return 0;
}