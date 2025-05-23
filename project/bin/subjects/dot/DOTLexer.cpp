
// Generated from DOT.g4 by ANTLR 4.13.2


#include "DOTLexer.h"


using namespace antlr4;



using namespace antlr4;

namespace {

struct DOTLexerStaticData final {
  DOTLexerStaticData(std::vector<std::string> ruleNames,
                          std::vector<std::string> channelNames,
                          std::vector<std::string> modeNames,
                          std::vector<std::string> literalNames,
                          std::vector<std::string> symbolicNames)
      : ruleNames(std::move(ruleNames)), channelNames(std::move(channelNames)),
        modeNames(std::move(modeNames)), literalNames(std::move(literalNames)),
        symbolicNames(std::move(symbolicNames)),
        vocabulary(this->literalNames, this->symbolicNames) {}

  DOTLexerStaticData(const DOTLexerStaticData&) = delete;
  DOTLexerStaticData(DOTLexerStaticData&&) = delete;
  DOTLexerStaticData& operator=(const DOTLexerStaticData&) = delete;
  DOTLexerStaticData& operator=(DOTLexerStaticData&&) = delete;

  std::vector<antlr4::dfa::DFA> decisionToDFA;
  antlr4::atn::PredictionContextCache sharedContextCache;
  const std::vector<std::string> ruleNames;
  const std::vector<std::string> channelNames;
  const std::vector<std::string> modeNames;
  const std::vector<std::string> literalNames;
  const std::vector<std::string> symbolicNames;
  const antlr4::dfa::Vocabulary vocabulary;
  antlr4::atn::SerializedATNView serializedATN;
  std::unique_ptr<antlr4::atn::ATN> atn;
};

::antlr4::internal::OnceFlag dotlexerLexerOnceFlag;
#if ANTLR4_USE_THREAD_LOCAL_CACHE
static thread_local
#endif
std::unique_ptr<DOTLexerStaticData> dotlexerLexerStaticData = nullptr;

void dotlexerLexerInitialize() {
#if ANTLR4_USE_THREAD_LOCAL_CACHE
  if (dotlexerLexerStaticData != nullptr) {
    return;
  }
#else
  assert(dotlexerLexerStaticData == nullptr);
#endif
  auto staticData = std::make_unique<DOTLexerStaticData>(
    std::vector<std::string>{
      "T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", "T__7", "T__8", 
      "T__9", "STRICT", "GRAPH", "DIGRAPH", "NODE", "EDGE", "SUBGRAPH", 
      "NUMBER", "DIGIT", "STRING", "ID", "LETTER", "HTML_STRING", "TAG", 
      "COMMENT", "LINE_COMMENT", "PREPROC", "WS"
    },
    std::vector<std::string>{
      "DEFAULT_TOKEN_CHANNEL", "HIDDEN"
    },
    std::vector<std::string>{
      "DEFAULT_MODE"
    },
    std::vector<std::string>{
      "", "'{'", "'}'", "';'", "'='", "'['", "']'", "','", "'->'", "'--'", 
      "':'"
    },
    std::vector<std::string>{
      "", "", "", "", "", "", "", "", "", "", "", "STRICT", "GRAPH", "DIGRAPH", 
      "NODE", "EDGE", "SUBGRAPH", "NUMBER", "STRING", "ID", "HTML_STRING", 
      "COMMENT", "LINE_COMMENT", "PREPROC", "WS"
    }
  );
  static const int32_t serializedATNSegment[] = {
  	4,0,24,230,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
  	6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,2,14,
  	7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,7,20,2,21,
  	7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,1,0,1,0,1,1,1,
  	1,1,2,1,2,1,3,1,3,1,4,1,4,1,5,1,5,1,6,1,6,1,7,1,7,1,7,1,8,1,8,1,8,1,9,
  	1,9,1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,11,1,11,1,11,1,11,1,11,1,11,
  	1,12,1,12,1,12,1,12,1,12,1,12,1,12,1,12,1,13,1,13,1,13,1,13,1,13,1,14,
  	1,14,1,14,1,14,1,14,1,15,1,15,1,15,1,15,1,15,1,15,1,15,1,15,1,15,1,16,
  	3,16,119,8,16,1,16,1,16,4,16,123,8,16,11,16,12,16,124,1,16,4,16,128,8,
  	16,11,16,12,16,129,1,16,1,16,5,16,134,8,16,10,16,12,16,137,9,16,3,16,
  	139,8,16,3,16,141,8,16,1,17,1,17,1,18,1,18,1,18,1,18,5,18,149,8,18,10,
  	18,12,18,152,9,18,1,18,1,18,1,19,1,19,1,19,5,19,159,8,19,10,19,12,19,
  	162,9,19,1,20,1,20,1,21,1,21,1,21,5,21,169,8,21,10,21,12,21,172,9,21,
  	1,21,1,21,1,22,1,22,5,22,178,8,22,10,22,12,22,181,9,22,1,22,1,22,1,23,
  	1,23,1,23,1,23,5,23,189,8,23,10,23,12,23,192,9,23,1,23,1,23,1,23,1,23,
  	1,23,1,24,1,24,1,24,1,24,5,24,203,8,24,10,24,12,24,206,9,24,1,24,3,24,
  	209,8,24,1,24,1,24,1,24,1,24,1,25,1,25,5,25,217,8,25,10,25,12,25,220,
  	9,25,1,25,1,25,1,26,4,26,225,8,26,11,26,12,26,226,1,26,1,26,4,150,179,
  	190,204,0,27,1,1,3,2,5,3,7,4,9,5,11,6,13,7,15,8,17,9,19,10,21,11,23,12,
  	25,13,27,14,29,15,31,16,33,17,35,0,37,18,39,19,41,0,43,20,45,0,47,21,
  	49,22,51,23,53,24,1,0,20,2,0,83,83,115,115,2,0,84,84,116,116,2,0,82,82,
  	114,114,2,0,73,73,105,105,2,0,67,67,99,99,2,0,71,71,103,103,2,0,65,65,
  	97,97,2,0,80,80,112,112,2,0,72,72,104,104,2,0,68,68,100,100,2,0,78,78,
  	110,110,2,0,79,79,111,111,2,0,69,69,101,101,2,0,85,85,117,117,2,0,66,
  	66,98,98,1,0,48,57,4,0,65,90,95,95,97,122,128,255,2,0,60,60,62,62,2,0,
  	10,10,13,13,3,0,9,10,13,13,32,32,244,0,1,1,0,0,0,0,3,1,0,0,0,0,5,1,0,
  	0,0,0,7,1,0,0,0,0,9,1,0,0,0,0,11,1,0,0,0,0,13,1,0,0,0,0,15,1,0,0,0,0,
  	17,1,0,0,0,0,19,1,0,0,0,0,21,1,0,0,0,0,23,1,0,0,0,0,25,1,0,0,0,0,27,1,
  	0,0,0,0,29,1,0,0,0,0,31,1,0,0,0,0,33,1,0,0,0,0,37,1,0,0,0,0,39,1,0,0,
  	0,0,43,1,0,0,0,0,47,1,0,0,0,0,49,1,0,0,0,0,51,1,0,0,0,0,53,1,0,0,0,1,
  	55,1,0,0,0,3,57,1,0,0,0,5,59,1,0,0,0,7,61,1,0,0,0,9,63,1,0,0,0,11,65,
  	1,0,0,0,13,67,1,0,0,0,15,69,1,0,0,0,17,72,1,0,0,0,19,75,1,0,0,0,21,77,
  	1,0,0,0,23,84,1,0,0,0,25,90,1,0,0,0,27,98,1,0,0,0,29,103,1,0,0,0,31,108,
  	1,0,0,0,33,118,1,0,0,0,35,142,1,0,0,0,37,144,1,0,0,0,39,155,1,0,0,0,41,
  	163,1,0,0,0,43,165,1,0,0,0,45,175,1,0,0,0,47,184,1,0,0,0,49,198,1,0,0,
  	0,51,214,1,0,0,0,53,224,1,0,0,0,55,56,5,123,0,0,56,2,1,0,0,0,57,58,5,
  	125,0,0,58,4,1,0,0,0,59,60,5,59,0,0,60,6,1,0,0,0,61,62,5,61,0,0,62,8,
  	1,0,0,0,63,64,5,91,0,0,64,10,1,0,0,0,65,66,5,93,0,0,66,12,1,0,0,0,67,
  	68,5,44,0,0,68,14,1,0,0,0,69,70,5,45,0,0,70,71,5,62,0,0,71,16,1,0,0,0,
  	72,73,5,45,0,0,73,74,5,45,0,0,74,18,1,0,0,0,75,76,5,58,0,0,76,20,1,0,
  	0,0,77,78,7,0,0,0,78,79,7,1,0,0,79,80,7,2,0,0,80,81,7,3,0,0,81,82,7,4,
  	0,0,82,83,7,1,0,0,83,22,1,0,0,0,84,85,7,5,0,0,85,86,7,2,0,0,86,87,7,6,
  	0,0,87,88,7,7,0,0,88,89,7,8,0,0,89,24,1,0,0,0,90,91,7,9,0,0,91,92,7,3,
  	0,0,92,93,7,5,0,0,93,94,7,2,0,0,94,95,7,6,0,0,95,96,7,7,0,0,96,97,7,8,
  	0,0,97,26,1,0,0,0,98,99,7,10,0,0,99,100,7,11,0,0,100,101,7,9,0,0,101,
  	102,7,12,0,0,102,28,1,0,0,0,103,104,7,12,0,0,104,105,7,9,0,0,105,106,
  	7,5,0,0,106,107,7,12,0,0,107,30,1,0,0,0,108,109,7,0,0,0,109,110,7,13,
  	0,0,110,111,7,14,0,0,111,112,7,5,0,0,112,113,7,2,0,0,113,114,7,6,0,0,
  	114,115,7,7,0,0,115,116,7,8,0,0,116,32,1,0,0,0,117,119,5,45,0,0,118,117,
  	1,0,0,0,118,119,1,0,0,0,119,140,1,0,0,0,120,122,5,46,0,0,121,123,3,35,
  	17,0,122,121,1,0,0,0,123,124,1,0,0,0,124,122,1,0,0,0,124,125,1,0,0,0,
  	125,141,1,0,0,0,126,128,3,35,17,0,127,126,1,0,0,0,128,129,1,0,0,0,129,
  	127,1,0,0,0,129,130,1,0,0,0,130,138,1,0,0,0,131,135,5,46,0,0,132,134,
  	3,35,17,0,133,132,1,0,0,0,134,137,1,0,0,0,135,133,1,0,0,0,135,136,1,0,
  	0,0,136,139,1,0,0,0,137,135,1,0,0,0,138,131,1,0,0,0,138,139,1,0,0,0,139,
  	141,1,0,0,0,140,120,1,0,0,0,140,127,1,0,0,0,141,34,1,0,0,0,142,143,7,
  	15,0,0,143,36,1,0,0,0,144,150,5,34,0,0,145,146,5,92,0,0,146,149,5,34,
  	0,0,147,149,9,0,0,0,148,145,1,0,0,0,148,147,1,0,0,0,149,152,1,0,0,0,150,
  	151,1,0,0,0,150,148,1,0,0,0,151,153,1,0,0,0,152,150,1,0,0,0,153,154,5,
  	34,0,0,154,38,1,0,0,0,155,160,3,41,20,0,156,159,3,41,20,0,157,159,3,35,
  	17,0,158,156,1,0,0,0,158,157,1,0,0,0,159,162,1,0,0,0,160,158,1,0,0,0,
  	160,161,1,0,0,0,161,40,1,0,0,0,162,160,1,0,0,0,163,164,7,16,0,0,164,42,
  	1,0,0,0,165,170,5,60,0,0,166,169,3,45,22,0,167,169,8,17,0,0,168,166,1,
  	0,0,0,168,167,1,0,0,0,169,172,1,0,0,0,170,168,1,0,0,0,170,171,1,0,0,0,
  	171,173,1,0,0,0,172,170,1,0,0,0,173,174,5,62,0,0,174,44,1,0,0,0,175,179,
  	5,60,0,0,176,178,9,0,0,0,177,176,1,0,0,0,178,181,1,0,0,0,179,180,1,0,
  	0,0,179,177,1,0,0,0,180,182,1,0,0,0,181,179,1,0,0,0,182,183,5,62,0,0,
  	183,46,1,0,0,0,184,185,5,47,0,0,185,186,5,42,0,0,186,190,1,0,0,0,187,
  	189,9,0,0,0,188,187,1,0,0,0,189,192,1,0,0,0,190,191,1,0,0,0,190,188,1,
  	0,0,0,191,193,1,0,0,0,192,190,1,0,0,0,193,194,5,42,0,0,194,195,5,47,0,
  	0,195,196,1,0,0,0,196,197,6,23,0,0,197,48,1,0,0,0,198,199,5,47,0,0,199,
  	200,5,47,0,0,200,204,1,0,0,0,201,203,9,0,0,0,202,201,1,0,0,0,203,206,
  	1,0,0,0,204,205,1,0,0,0,204,202,1,0,0,0,205,208,1,0,0,0,206,204,1,0,0,
  	0,207,209,5,13,0,0,208,207,1,0,0,0,208,209,1,0,0,0,209,210,1,0,0,0,210,
  	211,5,10,0,0,211,212,1,0,0,0,212,213,6,24,0,0,213,50,1,0,0,0,214,218,
  	5,35,0,0,215,217,8,18,0,0,216,215,1,0,0,0,217,220,1,0,0,0,218,216,1,0,
  	0,0,218,219,1,0,0,0,219,221,1,0,0,0,220,218,1,0,0,0,221,222,6,25,0,0,
  	222,52,1,0,0,0,223,225,7,19,0,0,224,223,1,0,0,0,225,226,1,0,0,0,226,224,
  	1,0,0,0,226,227,1,0,0,0,227,228,1,0,0,0,228,229,6,26,0,0,229,54,1,0,0,
  	0,19,0,118,124,129,135,138,140,148,150,158,160,168,170,179,190,204,208,
  	218,226,1,6,0,0
  };
  staticData->serializedATN = antlr4::atn::SerializedATNView(serializedATNSegment, sizeof(serializedATNSegment) / sizeof(serializedATNSegment[0]));

  antlr4::atn::ATNDeserializer deserializer;
  staticData->atn = deserializer.deserialize(staticData->serializedATN);

  const size_t count = staticData->atn->getNumberOfDecisions();
  staticData->decisionToDFA.reserve(count);
  for (size_t i = 0; i < count; i++) { 
    staticData->decisionToDFA.emplace_back(staticData->atn->getDecisionState(i), i);
  }
  dotlexerLexerStaticData = std::move(staticData);
}

}

DOTLexer::DOTLexer(CharStream *input) : Lexer(input) {
  DOTLexer::initialize();
  _interpreter = new atn::LexerATNSimulator(this, *dotlexerLexerStaticData->atn, dotlexerLexerStaticData->decisionToDFA, dotlexerLexerStaticData->sharedContextCache);
}

DOTLexer::~DOTLexer() {
  delete _interpreter;
}

std::string DOTLexer::getGrammarFileName() const {
  return "DOT.g4";
}

const std::vector<std::string>& DOTLexer::getRuleNames() const {
  return dotlexerLexerStaticData->ruleNames;
}

const std::vector<std::string>& DOTLexer::getChannelNames() const {
  return dotlexerLexerStaticData->channelNames;
}

const std::vector<std::string>& DOTLexer::getModeNames() const {
  return dotlexerLexerStaticData->modeNames;
}

const dfa::Vocabulary& DOTLexer::getVocabulary() const {
  return dotlexerLexerStaticData->vocabulary;
}

antlr4::atn::SerializedATNView DOTLexer::getSerializedATN() const {
  return dotlexerLexerStaticData->serializedATN;
}

const atn::ATN& DOTLexer::getATN() const {
  return *dotlexerLexerStaticData->atn;
}




void DOTLexer::initialize() {
#if ANTLR4_USE_THREAD_LOCAL_CACHE
  dotlexerLexerInitialize();
#else
  ::antlr4::internal::call_once(dotlexerLexerOnceFlag, dotlexerLexerInitialize);
#endif
}
