// ErrorListener.h
#pragma once
#include "antlr4-runtime.h"

class ExitCodeErrorListener : public antlr4::BaseErrorListener {
public:
    bool syntaxErrorSeen = false;
    bool eofOffending    = false;

    void syntaxError(antlr4::Recognizer*,
                     antlr4::Token* offendingSymbol,
                     size_t, size_t,
                     const std::string&,
                     std::exception_ptr) override
    {
        syntaxErrorSeen = true;
        if (offendingSymbol &&
            offendingSymbol->getType() == antlr4::Token::EOF)
            eofOffending = true;          // 输入意外结束
    }
};