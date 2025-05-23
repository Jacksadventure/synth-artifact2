// Generated from DOT.g4 by ANTLR 4.9.2
package erepair.program.generated;
import org.antlr.v4.runtime.Lexer;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.TokenStream;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.misc.*;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class DOTLexer extends Lexer {
	static { RuntimeMetaData.checkVersion("4.9.2", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, T__1=2, T__2=3, T__3=4, T__4=5, T__5=6, T__6=7, T__7=8, T__8=9, 
		T__9=10, STRICT=11, GRAPH=12, DIGRAPH=13, NODE=14, EDGE=15, SUBGRAPH=16, 
		NUMBER=17, STRING=18, ID=19, HTML_STRING=20, COMMENT=21, LINE_COMMENT=22, 
		PREPROC=23, WS=24;
	public static String[] channelNames = {
		"DEFAULT_TOKEN_CHANNEL", "HIDDEN"
	};

	public static String[] modeNames = {
		"DEFAULT_MODE"
	};

	private static String[] makeRuleNames() {
		return new String[] {
			"T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", "T__7", "T__8", 
			"T__9", "STRICT", "GRAPH", "DIGRAPH", "NODE", "EDGE", "SUBGRAPH", "NUMBER", 
			"DIGIT", "STRING", "ID", "LETTER", "HTML_STRING", "TAG", "COMMENT", "LINE_COMMENT", 
			"PREPROC", "WS"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'{'", "'}'", "';'", "'='", "'['", "']'", "','", "'->'", "'--'", 
			"':'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, null, null, null, null, null, null, null, null, null, "STRICT", 
			"GRAPH", "DIGRAPH", "NODE", "EDGE", "SUBGRAPH", "NUMBER", "STRING", "ID", 
			"HTML_STRING", "COMMENT", "LINE_COMMENT", "PREPROC", "WS"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}


	public DOTLexer(CharStream input) {
		super(input);
		_interp = new LexerATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@Override
	public String getGrammarFileName() { return "DOT.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public String[] getChannelNames() { return channelNames; }

	@Override
	public String[] getModeNames() { return modeNames; }

	@Override
	public ATN getATN() { return _ATN; }

	public static final String _serializedATN =
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\32\u00e8\b\1\4\2"+
		"\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4"+
		"\13\t\13\4\f\t\f\4\r\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22"+
		"\t\22\4\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30\4\31"+
		"\t\31\4\32\t\32\4\33\t\33\4\34\t\34\3\2\3\2\3\3\3\3\3\4\3\4\3\5\3\5\3"+
		"\6\3\6\3\7\3\7\3\b\3\b\3\t\3\t\3\t\3\n\3\n\3\n\3\13\3\13\3\f\3\f\3\f\3"+
		"\f\3\f\3\f\3\f\3\r\3\r\3\r\3\r\3\r\3\r\3\16\3\16\3\16\3\16\3\16\3\16\3"+
		"\16\3\16\3\17\3\17\3\17\3\17\3\17\3\20\3\20\3\20\3\20\3\20\3\21\3\21\3"+
		"\21\3\21\3\21\3\21\3\21\3\21\3\21\3\22\5\22y\n\22\3\22\3\22\6\22}\n\22"+
		"\r\22\16\22~\3\22\6\22\u0082\n\22\r\22\16\22\u0083\3\22\3\22\7\22\u0088"+
		"\n\22\f\22\16\22\u008b\13\22\5\22\u008d\n\22\5\22\u008f\n\22\3\23\3\23"+
		"\3\24\3\24\3\24\3\24\7\24\u0097\n\24\f\24\16\24\u009a\13\24\3\24\3\24"+
		"\3\25\3\25\3\25\7\25\u00a1\n\25\f\25\16\25\u00a4\13\25\3\26\3\26\3\27"+
		"\3\27\3\27\7\27\u00ab\n\27\f\27\16\27\u00ae\13\27\3\27\3\27\3\30\3\30"+
		"\7\30\u00b4\n\30\f\30\16\30\u00b7\13\30\3\30\3\30\3\31\3\31\3\31\3\31"+
		"\7\31\u00bf\n\31\f\31\16\31\u00c2\13\31\3\31\3\31\3\31\3\31\3\31\3\32"+
		"\3\32\3\32\3\32\7\32\u00cd\n\32\f\32\16\32\u00d0\13\32\3\32\5\32\u00d3"+
		"\n\32\3\32\3\32\3\32\3\32\3\33\3\33\7\33\u00db\n\33\f\33\16\33\u00de\13"+
		"\33\3\33\3\33\3\34\6\34\u00e3\n\34\r\34\16\34\u00e4\3\34\3\34\6\u0098"+
		"\u00b5\u00c0\u00ce\2\35\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f"+
		"\27\r\31\16\33\17\35\20\37\21!\22#\23%\2\'\24)\25+\2-\26/\2\61\27\63\30"+
		"\65\31\67\32\3\2\26\4\2UUuu\4\2VVvv\4\2TTtt\4\2KKkk\4\2EEee\4\2IIii\4"+
		"\2CCcc\4\2RRrr\4\2JJjj\4\2FFff\4\2PPpp\4\2QQqq\4\2GGgg\4\2WWww\4\2DDd"+
		"d\3\2\62;\6\2C\\aac|\u0082\u0101\4\2>>@@\4\2\f\f\17\17\5\2\13\f\17\17"+
		"\"\"\2\u00f6\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2\2\2\t\3\2\2\2\2\13\3\2"+
		"\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2\2"+
		"\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\2\37\3\2\2\2\2!\3\2"+
		"\2\2\2#\3\2\2\2\2\'\3\2\2\2\2)\3\2\2\2\2-\3\2\2\2\2\61\3\2\2\2\2\63\3"+
		"\2\2\2\2\65\3\2\2\2\2\67\3\2\2\2\39\3\2\2\2\5;\3\2\2\2\7=\3\2\2\2\t?\3"+
		"\2\2\2\13A\3\2\2\2\rC\3\2\2\2\17E\3\2\2\2\21G\3\2\2\2\23J\3\2\2\2\25M"+
		"\3\2\2\2\27O\3\2\2\2\31V\3\2\2\2\33\\\3\2\2\2\35d\3\2\2\2\37i\3\2\2\2"+
		"!n\3\2\2\2#x\3\2\2\2%\u0090\3\2\2\2\'\u0092\3\2\2\2)\u009d\3\2\2\2+\u00a5"+
		"\3\2\2\2-\u00a7\3\2\2\2/\u00b1\3\2\2\2\61\u00ba\3\2\2\2\63\u00c8\3\2\2"+
		"\2\65\u00d8\3\2\2\2\67\u00e2\3\2\2\29:\7}\2\2:\4\3\2\2\2;<\7\177\2\2<"+
		"\6\3\2\2\2=>\7=\2\2>\b\3\2\2\2?@\7?\2\2@\n\3\2\2\2AB\7]\2\2B\f\3\2\2\2"+
		"CD\7_\2\2D\16\3\2\2\2EF\7.\2\2F\20\3\2\2\2GH\7/\2\2HI\7@\2\2I\22\3\2\2"+
		"\2JK\7/\2\2KL\7/\2\2L\24\3\2\2\2MN\7<\2\2N\26\3\2\2\2OP\t\2\2\2PQ\t\3"+
		"\2\2QR\t\4\2\2RS\t\5\2\2ST\t\6\2\2TU\t\3\2\2U\30\3\2\2\2VW\t\7\2\2WX\t"+
		"\4\2\2XY\t\b\2\2YZ\t\t\2\2Z[\t\n\2\2[\32\3\2\2\2\\]\t\13\2\2]^\t\5\2\2"+
		"^_\t\7\2\2_`\t\4\2\2`a\t\b\2\2ab\t\t\2\2bc\t\n\2\2c\34\3\2\2\2de\t\f\2"+
		"\2ef\t\r\2\2fg\t\13\2\2gh\t\16\2\2h\36\3\2\2\2ij\t\16\2\2jk\t\13\2\2k"+
		"l\t\7\2\2lm\t\16\2\2m \3\2\2\2no\t\2\2\2op\t\17\2\2pq\t\20\2\2qr\t\7\2"+
		"\2rs\t\4\2\2st\t\b\2\2tu\t\t\2\2uv\t\n\2\2v\"\3\2\2\2wy\7/\2\2xw\3\2\2"+
		"\2xy\3\2\2\2y\u008e\3\2\2\2z|\7\60\2\2{}\5%\23\2|{\3\2\2\2}~\3\2\2\2~"+
		"|\3\2\2\2~\177\3\2\2\2\177\u008f\3\2\2\2\u0080\u0082\5%\23\2\u0081\u0080"+
		"\3\2\2\2\u0082\u0083\3\2\2\2\u0083\u0081\3\2\2\2\u0083\u0084\3\2\2\2\u0084"+
		"\u008c\3\2\2\2\u0085\u0089\7\60\2\2\u0086\u0088\5%\23\2\u0087\u0086\3"+
		"\2\2\2\u0088\u008b\3\2\2\2\u0089\u0087\3\2\2\2\u0089\u008a\3\2\2\2\u008a"+
		"\u008d\3\2\2\2\u008b\u0089\3\2\2\2\u008c\u0085\3\2\2\2\u008c\u008d\3\2"+
		"\2\2\u008d\u008f\3\2\2\2\u008ez\3\2\2\2\u008e\u0081\3\2\2\2\u008f$\3\2"+
		"\2\2\u0090\u0091\t\21\2\2\u0091&\3\2\2\2\u0092\u0098\7$\2\2\u0093\u0094"+
		"\7^\2\2\u0094\u0097\7$\2\2\u0095\u0097\13\2\2\2\u0096\u0093\3\2\2\2\u0096"+
		"\u0095\3\2\2\2\u0097\u009a\3\2\2\2\u0098\u0099\3\2\2\2\u0098\u0096\3\2"+
		"\2\2\u0099\u009b\3\2\2\2\u009a\u0098\3\2\2\2\u009b\u009c\7$\2\2\u009c"+
		"(\3\2\2\2\u009d\u00a2\5+\26\2\u009e\u00a1\5+\26\2\u009f\u00a1\5%\23\2"+
		"\u00a0\u009e\3\2\2\2\u00a0\u009f\3\2\2\2\u00a1\u00a4\3\2\2\2\u00a2\u00a0"+
		"\3\2\2\2\u00a2\u00a3\3\2\2\2\u00a3*\3\2\2\2\u00a4\u00a2\3\2\2\2\u00a5"+
		"\u00a6\t\22\2\2\u00a6,\3\2\2\2\u00a7\u00ac\7>\2\2\u00a8\u00ab\5/\30\2"+
		"\u00a9\u00ab\n\23\2\2\u00aa\u00a8\3\2\2\2\u00aa\u00a9\3\2\2\2\u00ab\u00ae"+
		"\3\2\2\2\u00ac\u00aa\3\2\2\2\u00ac\u00ad\3\2\2\2\u00ad\u00af\3\2\2\2\u00ae"+
		"\u00ac\3\2\2\2\u00af\u00b0\7@\2\2\u00b0.\3\2\2\2\u00b1\u00b5\7>\2\2\u00b2"+
		"\u00b4\13\2\2\2\u00b3\u00b2\3\2\2\2\u00b4\u00b7\3\2\2\2\u00b5\u00b6\3"+
		"\2\2\2\u00b5\u00b3\3\2\2\2\u00b6\u00b8\3\2\2\2\u00b7\u00b5\3\2\2\2\u00b8"+
		"\u00b9\7@\2\2\u00b9\60\3\2\2\2\u00ba\u00bb\7\61\2\2\u00bb\u00bc\7,\2\2"+
		"\u00bc\u00c0\3\2\2\2\u00bd\u00bf\13\2\2\2\u00be\u00bd\3\2\2\2\u00bf\u00c2"+
		"\3\2\2\2\u00c0\u00c1\3\2\2\2\u00c0\u00be\3\2\2\2\u00c1\u00c3\3\2\2\2\u00c2"+
		"\u00c0\3\2\2\2\u00c3\u00c4\7,\2\2\u00c4\u00c5\7\61\2\2\u00c5\u00c6\3\2"+
		"\2\2\u00c6\u00c7\b\31\2\2\u00c7\62\3\2\2\2\u00c8\u00c9\7\61\2\2\u00c9"+
		"\u00ca\7\61\2\2\u00ca\u00ce\3\2\2\2\u00cb\u00cd\13\2\2\2\u00cc\u00cb\3"+
		"\2\2\2\u00cd\u00d0\3\2\2\2\u00ce\u00cf\3\2\2\2\u00ce\u00cc\3\2\2\2\u00cf"+
		"\u00d2\3\2\2\2\u00d0\u00ce\3\2\2\2\u00d1\u00d3\7\17\2\2\u00d2\u00d1\3"+
		"\2\2\2\u00d2\u00d3\3\2\2\2\u00d3\u00d4\3\2\2\2\u00d4\u00d5\7\f\2\2\u00d5"+
		"\u00d6\3\2\2\2\u00d6\u00d7\b\32\2\2\u00d7\64\3\2\2\2\u00d8\u00dc\7%\2"+
		"\2\u00d9\u00db\n\24\2\2\u00da\u00d9\3\2\2\2\u00db\u00de\3\2\2\2\u00dc"+
		"\u00da\3\2\2\2\u00dc\u00dd\3\2\2\2\u00dd\u00df\3\2\2\2\u00de\u00dc\3\2"+
		"\2\2\u00df\u00e0\b\33\2\2\u00e0\66\3\2\2\2\u00e1\u00e3\t\25\2\2\u00e2"+
		"\u00e1\3\2\2\2\u00e3\u00e4\3\2\2\2\u00e4\u00e2\3\2\2\2\u00e4\u00e5\3\2"+
		"\2\2\u00e5\u00e6\3\2\2\2\u00e6\u00e7\b\34\2\2\u00e78\3\2\2\2\25\2x~\u0083"+
		"\u0089\u008c\u008e\u0096\u0098\u00a0\u00a2\u00aa\u00ac\u00b5\u00c0\u00ce"+
		"\u00d2\u00dc\u00e4\3\b\2\2";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}