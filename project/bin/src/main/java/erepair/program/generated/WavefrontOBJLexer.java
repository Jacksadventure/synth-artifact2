// Generated from WavefrontOBJ.g4 by ANTLR 4.9.2
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
public class WavefrontOBJLexer extends Lexer {
	static { RuntimeMetaData.checkVersion("4.9.2", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, T__1=2, T__2=3, T__3=4, T__4=5, T__5=6, T__6=7, T__7=8, T__8=9, 
		T__9=10, T__10=11, T__11=12, T__12=13, T__13=14, T__14=15, T__15=16, T__16=17, 
		T__17=18, T__18=19, T__19=20, T__20=21, T__21=22, T__22=23, T__23=24, 
		T__24=25, T__25=26, T__26=27, T__27=28, T__28=29, T__29=30, T__30=31, 
		T__31=32, T__32=33, T__33=34, T__34=35, T__35=36, T__36=37, T__37=38, 
		T__38=39, T__39=40, T__40=41, T__41=42, T__42=43, T__43=44, T__44=45, 
		T__45=46, T__46=47, T__47=48, T__48=49, T__49=50, T__50=51, INTEGER_PAIR=52, 
		INTEGER_TRIPLET=53, INTEGER=54, DECIMAL=55, COMMENT=56, NAME=57, FILENAME=58, 
		WS=59, NL=60, NON_NL=61, NON_WS=62;
	public static String[] channelNames = {
		"DEFAULT_TOKEN_CHANNEL", "HIDDEN"
	};

	public static String[] modeNames = {
		"DEFAULT_MODE"
	};

	private static String[] makeRuleNames() {
		return new String[] {
			"T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", "T__7", "T__8", 
			"T__9", "T__10", "T__11", "T__12", "T__13", "T__14", "T__15", "T__16", 
			"T__17", "T__18", "T__19", "T__20", "T__21", "T__22", "T__23", "T__24", 
			"T__25", "T__26", "T__27", "T__28", "T__29", "T__30", "T__31", "T__32", 
			"T__33", "T__34", "T__35", "T__36", "T__37", "T__38", "T__39", "T__40", 
			"T__41", "T__42", "T__43", "T__44", "T__45", "T__46", "T__47", "T__48", 
			"T__49", "T__50", "INTEGER_PAIR", "INTEGER_TRIPLET", "INTEGER", "DECIMAL", 
			"DIGIT", "COMMENT", "NAME", "FILENAME", "WS", "NL", "NON_NL", "NON_WS"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'-'", "'v'", "'vp'", "'vn'", "'vt'", "'cstype'", "'rat'", "'bmatrix'", 
			"'bezier'", "'bspline'", "'cardinal'", "'taylor'", "'deg'", "'bmat'", 
			"'u'", "'step'", "'p'", "'l'", "'f'", "'curv'", "'curv2'", "'surf'", 
			"'parm'", "'trim'", "'hole'", "'scrv'", "'sp'", "'end'", "'con'", "'g'", 
			"'s'", "'off'", "'mg'", "'o'", "'bevel'", "'on'", "'c_interp'", "'d_interp'", 
			"'lod'", "'maplib'", "'usemap'", "'mtllib'", "'usemtl'", "'shadow_obj'", 
			"'trace_obj'", "'ctech'", "'cparm'", "'cspace'", "'stech'", "'cparma'", 
			"'cparmb'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, "INTEGER_PAIR", "INTEGER_TRIPLET", "INTEGER", 
			"DECIMAL", "COMMENT", "NAME", "FILENAME", "WS", "NL", "NON_NL", "NON_WS"
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


	public WavefrontOBJLexer(CharStream input) {
		super(input);
		_interp = new LexerATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@Override
	public String getGrammarFileName() { return "WavefrontOBJ.g4"; }

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
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2@\u01d7\b\1\4\2\t"+
		"\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13"+
		"\t\13\4\f\t\f\4\r\t\r\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22"+
		"\4\23\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30\4\31\t\31"+
		"\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36\t\36\4\37\t\37\4 \t \4!"+
		"\t!\4\"\t\"\4#\t#\4$\t$\4%\t%\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4"+
		",\t,\4-\t-\4.\t.\4/\t/\4\60\t\60\4\61\t\61\4\62\t\62\4\63\t\63\4\64\t"+
		"\64\4\65\t\65\4\66\t\66\4\67\t\67\48\t8\49\t9\4:\t:\4;\t;\4<\t<\4=\t="+
		"\4>\t>\4?\t?\4@\t@\3\2\3\2\3\3\3\3\3\4\3\4\3\4\3\5\3\5\3\5\3\6\3\6\3\6"+
		"\3\7\3\7\3\7\3\7\3\7\3\7\3\7\3\b\3\b\3\b\3\b\3\t\3\t\3\t\3\t\3\t\3\t\3"+
		"\t\3\t\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\13\3\13\3\13\3\13\3\13\3\13\3\13"+
		"\3\13\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\f\3\r\3\r\3\r\3\r\3\r\3\r\3\r"+
		"\3\16\3\16\3\16\3\16\3\17\3\17\3\17\3\17\3\17\3\20\3\20\3\21\3\21\3\21"+
		"\3\21\3\21\3\22\3\22\3\23\3\23\3\24\3\24\3\25\3\25\3\25\3\25\3\25\3\26"+
		"\3\26\3\26\3\26\3\26\3\26\3\27\3\27\3\27\3\27\3\27\3\30\3\30\3\30\3\30"+
		"\3\30\3\31\3\31\3\31\3\31\3\31\3\32\3\32\3\32\3\32\3\32\3\33\3\33\3\33"+
		"\3\33\3\33\3\34\3\34\3\34\3\35\3\35\3\35\3\35\3\36\3\36\3\36\3\36\3\37"+
		"\3\37\3 \3 \3!\3!\3!\3!\3\"\3\"\3\"\3#\3#\3$\3$\3$\3$\3$\3$\3%\3%\3%\3"+
		"&\3&\3&\3&\3&\3&\3&\3&\3&\3\'\3\'\3\'\3\'\3\'\3\'\3\'\3\'\3\'\3(\3(\3"+
		"(\3(\3)\3)\3)\3)\3)\3)\3)\3*\3*\3*\3*\3*\3*\3*\3+\3+\3+\3+\3+\3+\3+\3"+
		",\3,\3,\3,\3,\3,\3,\3-\3-\3-\3-\3-\3-\3-\3-\3-\3-\3-\3.\3.\3.\3.\3.\3"+
		".\3.\3.\3.\3.\3/\3/\3/\3/\3/\3/\3\60\3\60\3\60\3\60\3\60\3\60\3\61\3\61"+
		"\3\61\3\61\3\61\3\61\3\61\3\62\3\62\3\62\3\62\3\62\3\62\3\63\3\63\3\63"+
		"\3\63\3\63\3\63\3\63\3\64\3\64\3\64\3\64\3\64\3\64\3\64\3\65\3\65\3\65"+
		"\3\65\3\66\3\66\3\66\5\66\u0191\n\66\3\66\3\66\3\66\3\67\5\67\u0197\n"+
		"\67\3\67\6\67\u019a\n\67\r\67\16\67\u019b\38\38\38\78\u01a1\n8\f8\168"+
		"\u01a4\138\58\u01a6\n8\39\39\3:\3:\7:\u01ac\n:\f:\16:\u01af\13:\3:\3:"+
		"\5:\u01b3\n:\3:\3:\3;\6;\u01b8\n;\r;\16;\u01b9\3<\6<\u01bd\n<\r<\16<\u01be"+
		"\3=\3=\3=\6=\u01c4\n=\r=\16=\u01c5\3=\3=\3>\3>\5>\u01cc\n>\3>\5>\u01cf"+
		"\n>\3?\3?\3@\6@\u01d4\n@\r@\16@\u01d5\2\2A\3\3\5\4\7\5\t\6\13\7\r\b\17"+
		"\t\21\n\23\13\25\f\27\r\31\16\33\17\35\20\37\21!\22#\23%\24\'\25)\26+"+
		"\27-\30/\31\61\32\63\33\65\34\67\359\36;\37= ?!A\"C#E$G%I&K\'M(O)Q*S+"+
		"U,W-Y.[/]\60_\61a\62c\63e\64g\65i\66k\67m8o9q\2s:u;w<y={>}?\177@\3\2\7"+
		"\t\2*+//\62;C\\aac|\u0080\u0080\6\2\13\f\17\17\"\"\61\61\4\2\13\13\"\""+
		"\4\2\f\f\17\17\5\2\13\f\17\17\"\"\2\u01e3\2\3\3\2\2\2\2\5\3\2\2\2\2\7"+
		"\3\2\2\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2\21\3\2\2"+
		"\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31\3\2\2\2\2\33\3\2\2\2\2"+
		"\35\3\2\2\2\2\37\3\2\2\2\2!\3\2\2\2\2#\3\2\2\2\2%\3\2\2\2\2\'\3\2\2\2"+
		"\2)\3\2\2\2\2+\3\2\2\2\2-\3\2\2\2\2/\3\2\2\2\2\61\3\2\2\2\2\63\3\2\2\2"+
		"\2\65\3\2\2\2\2\67\3\2\2\2\29\3\2\2\2\2;\3\2\2\2\2=\3\2\2\2\2?\3\2\2\2"+
		"\2A\3\2\2\2\2C\3\2\2\2\2E\3\2\2\2\2G\3\2\2\2\2I\3\2\2\2\2K\3\2\2\2\2M"+
		"\3\2\2\2\2O\3\2\2\2\2Q\3\2\2\2\2S\3\2\2\2\2U\3\2\2\2\2W\3\2\2\2\2Y\3\2"+
		"\2\2\2[\3\2\2\2\2]\3\2\2\2\2_\3\2\2\2\2a\3\2\2\2\2c\3\2\2\2\2e\3\2\2\2"+
		"\2g\3\2\2\2\2i\3\2\2\2\2k\3\2\2\2\2m\3\2\2\2\2o\3\2\2\2\2s\3\2\2\2\2u"+
		"\3\2\2\2\2w\3\2\2\2\2y\3\2\2\2\2{\3\2\2\2\2}\3\2\2\2\2\177\3\2\2\2\3\u0081"+
		"\3\2\2\2\5\u0083\3\2\2\2\7\u0085\3\2\2\2\t\u0088\3\2\2\2\13\u008b\3\2"+
		"\2\2\r\u008e\3\2\2\2\17\u0095\3\2\2\2\21\u0099\3\2\2\2\23\u00a1\3\2\2"+
		"\2\25\u00a8\3\2\2\2\27\u00b0\3\2\2\2\31\u00b9\3\2\2\2\33\u00c0\3\2\2\2"+
		"\35\u00c4\3\2\2\2\37\u00c9\3\2\2\2!\u00cb\3\2\2\2#\u00d0\3\2\2\2%\u00d2"+
		"\3\2\2\2\'\u00d4\3\2\2\2)\u00d6\3\2\2\2+\u00db\3\2\2\2-\u00e1\3\2\2\2"+
		"/\u00e6\3\2\2\2\61\u00eb\3\2\2\2\63\u00f0\3\2\2\2\65\u00f5\3\2\2\2\67"+
		"\u00fa\3\2\2\29\u00fd\3\2\2\2;\u0101\3\2\2\2=\u0105\3\2\2\2?\u0107\3\2"+
		"\2\2A\u0109\3\2\2\2C\u010d\3\2\2\2E\u0110\3\2\2\2G\u0112\3\2\2\2I\u0118"+
		"\3\2\2\2K\u011b\3\2\2\2M\u0124\3\2\2\2O\u012d\3\2\2\2Q\u0131\3\2\2\2S"+
		"\u0138\3\2\2\2U\u013f\3\2\2\2W\u0146\3\2\2\2Y\u014d\3\2\2\2[\u0158\3\2"+
		"\2\2]\u0162\3\2\2\2_\u0168\3\2\2\2a\u016e\3\2\2\2c\u0175\3\2\2\2e\u017b"+
		"\3\2\2\2g\u0182\3\2\2\2i\u0189\3\2\2\2k\u018d\3\2\2\2m\u0196\3\2\2\2o"+
		"\u019d\3\2\2\2q\u01a7\3\2\2\2s\u01a9\3\2\2\2u\u01b7\3\2\2\2w\u01bc\3\2"+
		"\2\2y\u01c3\3\2\2\2{\u01ce\3\2\2\2}\u01d0\3\2\2\2\177\u01d3\3\2\2\2\u0081"+
		"\u0082\7/\2\2\u0082\4\3\2\2\2\u0083\u0084\7x\2\2\u0084\6\3\2\2\2\u0085"+
		"\u0086\7x\2\2\u0086\u0087\7r\2\2\u0087\b\3\2\2\2\u0088\u0089\7x\2\2\u0089"+
		"\u008a\7p\2\2\u008a\n\3\2\2\2\u008b\u008c\7x\2\2\u008c\u008d\7v\2\2\u008d"+
		"\f\3\2\2\2\u008e\u008f\7e\2\2\u008f\u0090\7u\2\2\u0090\u0091\7v\2\2\u0091"+
		"\u0092\7{\2\2\u0092\u0093\7r\2\2\u0093\u0094\7g\2\2\u0094\16\3\2\2\2\u0095"+
		"\u0096\7t\2\2\u0096\u0097\7c\2\2\u0097\u0098\7v\2\2\u0098\20\3\2\2\2\u0099"+
		"\u009a\7d\2\2\u009a\u009b\7o\2\2\u009b\u009c\7c\2\2\u009c\u009d\7v\2\2"+
		"\u009d\u009e\7t\2\2\u009e\u009f\7k\2\2\u009f\u00a0\7z\2\2\u00a0\22\3\2"+
		"\2\2\u00a1\u00a2\7d\2\2\u00a2\u00a3\7g\2\2\u00a3\u00a4\7|\2\2\u00a4\u00a5"+
		"\7k\2\2\u00a5\u00a6\7g\2\2\u00a6\u00a7\7t\2\2\u00a7\24\3\2\2\2\u00a8\u00a9"+
		"\7d\2\2\u00a9\u00aa\7u\2\2\u00aa\u00ab\7r\2\2\u00ab\u00ac\7n\2\2\u00ac"+
		"\u00ad\7k\2\2\u00ad\u00ae\7p\2\2\u00ae\u00af\7g\2\2\u00af\26\3\2\2\2\u00b0"+
		"\u00b1\7e\2\2\u00b1\u00b2\7c\2\2\u00b2\u00b3\7t\2\2\u00b3\u00b4\7f\2\2"+
		"\u00b4\u00b5\7k\2\2\u00b5\u00b6\7p\2\2\u00b6\u00b7\7c\2\2\u00b7\u00b8"+
		"\7n\2\2\u00b8\30\3\2\2\2\u00b9\u00ba\7v\2\2\u00ba\u00bb\7c\2\2\u00bb\u00bc"+
		"\7{\2\2\u00bc\u00bd\7n\2\2\u00bd\u00be\7q\2\2\u00be\u00bf\7t\2\2\u00bf"+
		"\32\3\2\2\2\u00c0\u00c1\7f\2\2\u00c1\u00c2\7g\2\2\u00c2\u00c3\7i\2\2\u00c3"+
		"\34\3\2\2\2\u00c4\u00c5\7d\2\2\u00c5\u00c6\7o\2\2\u00c6\u00c7\7c\2\2\u00c7"+
		"\u00c8\7v\2\2\u00c8\36\3\2\2\2\u00c9\u00ca\7w\2\2\u00ca \3\2\2\2\u00cb"+
		"\u00cc\7u\2\2\u00cc\u00cd\7v\2\2\u00cd\u00ce\7g\2\2\u00ce\u00cf\7r\2\2"+
		"\u00cf\"\3\2\2\2\u00d0\u00d1\7r\2\2\u00d1$\3\2\2\2\u00d2\u00d3\7n\2\2"+
		"\u00d3&\3\2\2\2\u00d4\u00d5\7h\2\2\u00d5(\3\2\2\2\u00d6\u00d7\7e\2\2\u00d7"+
		"\u00d8\7w\2\2\u00d8\u00d9\7t\2\2\u00d9\u00da\7x\2\2\u00da*\3\2\2\2\u00db"+
		"\u00dc\7e\2\2\u00dc\u00dd\7w\2\2\u00dd\u00de\7t\2\2\u00de\u00df\7x\2\2"+
		"\u00df\u00e0\7\64\2\2\u00e0,\3\2\2\2\u00e1\u00e2\7u\2\2\u00e2\u00e3\7"+
		"w\2\2\u00e3\u00e4\7t\2\2\u00e4\u00e5\7h\2\2\u00e5.\3\2\2\2\u00e6\u00e7"+
		"\7r\2\2\u00e7\u00e8\7c\2\2\u00e8\u00e9\7t\2\2\u00e9\u00ea\7o\2\2\u00ea"+
		"\60\3\2\2\2\u00eb\u00ec\7v\2\2\u00ec\u00ed\7t\2\2\u00ed\u00ee\7k\2\2\u00ee"+
		"\u00ef\7o\2\2\u00ef\62\3\2\2\2\u00f0\u00f1\7j\2\2\u00f1\u00f2\7q\2\2\u00f2"+
		"\u00f3\7n\2\2\u00f3\u00f4\7g\2\2\u00f4\64\3\2\2\2\u00f5\u00f6\7u\2\2\u00f6"+
		"\u00f7\7e\2\2\u00f7\u00f8\7t\2\2\u00f8\u00f9\7x\2\2\u00f9\66\3\2\2\2\u00fa"+
		"\u00fb\7u\2\2\u00fb\u00fc\7r\2\2\u00fc8\3\2\2\2\u00fd\u00fe\7g\2\2\u00fe"+
		"\u00ff\7p\2\2\u00ff\u0100\7f\2\2\u0100:\3\2\2\2\u0101\u0102\7e\2\2\u0102"+
		"\u0103\7q\2\2\u0103\u0104\7p\2\2\u0104<\3\2\2\2\u0105\u0106\7i\2\2\u0106"+
		">\3\2\2\2\u0107\u0108\7u\2\2\u0108@\3\2\2\2\u0109\u010a\7q\2\2\u010a\u010b"+
		"\7h\2\2\u010b\u010c\7h\2\2\u010cB\3\2\2\2\u010d\u010e\7o\2\2\u010e\u010f"+
		"\7i\2\2\u010fD\3\2\2\2\u0110\u0111\7q\2\2\u0111F\3\2\2\2\u0112\u0113\7"+
		"d\2\2\u0113\u0114\7g\2\2\u0114\u0115\7x\2\2\u0115\u0116\7g\2\2\u0116\u0117"+
		"\7n\2\2\u0117H\3\2\2\2\u0118\u0119\7q\2\2\u0119\u011a\7p\2\2\u011aJ\3"+
		"\2\2\2\u011b\u011c\7e\2\2\u011c\u011d\7a\2\2\u011d\u011e\7k\2\2\u011e"+
		"\u011f\7p\2\2\u011f\u0120\7v\2\2\u0120\u0121\7g\2\2\u0121\u0122\7t\2\2"+
		"\u0122\u0123\7r\2\2\u0123L\3\2\2\2\u0124\u0125\7f\2\2\u0125\u0126\7a\2"+
		"\2\u0126\u0127\7k\2\2\u0127\u0128\7p\2\2\u0128\u0129\7v\2\2\u0129\u012a"+
		"\7g\2\2\u012a\u012b\7t\2\2\u012b\u012c\7r\2\2\u012cN\3\2\2\2\u012d\u012e"+
		"\7n\2\2\u012e\u012f\7q\2\2\u012f\u0130\7f\2\2\u0130P\3\2\2\2\u0131\u0132"+
		"\7o\2\2\u0132\u0133\7c\2\2\u0133\u0134\7r\2\2\u0134\u0135\7n\2\2\u0135"+
		"\u0136\7k\2\2\u0136\u0137\7d\2\2\u0137R\3\2\2\2\u0138\u0139\7w\2\2\u0139"+
		"\u013a\7u\2\2\u013a\u013b\7g\2\2\u013b\u013c\7o\2\2\u013c\u013d\7c\2\2"+
		"\u013d\u013e\7r\2\2\u013eT\3\2\2\2\u013f\u0140\7o\2\2\u0140\u0141\7v\2"+
		"\2\u0141\u0142\7n\2\2\u0142\u0143\7n\2\2\u0143\u0144\7k\2\2\u0144\u0145"+
		"\7d\2\2\u0145V\3\2\2\2\u0146\u0147\7w\2\2\u0147\u0148\7u\2\2\u0148\u0149"+
		"\7g\2\2\u0149\u014a\7o\2\2\u014a\u014b\7v\2\2\u014b\u014c\7n\2\2\u014c"+
		"X\3\2\2\2\u014d\u014e\7u\2\2\u014e\u014f\7j\2\2\u014f\u0150\7c\2\2\u0150"+
		"\u0151\7f\2\2\u0151\u0152\7q\2\2\u0152\u0153\7y\2\2\u0153\u0154\7a\2\2"+
		"\u0154\u0155\7q\2\2\u0155\u0156\7d\2\2\u0156\u0157\7l\2\2\u0157Z\3\2\2"+
		"\2\u0158\u0159\7v\2\2\u0159\u015a\7t\2\2\u015a\u015b\7c\2\2\u015b\u015c"+
		"\7e\2\2\u015c\u015d\7g\2\2\u015d\u015e\7a\2\2\u015e\u015f\7q\2\2\u015f"+
		"\u0160\7d\2\2\u0160\u0161\7l\2\2\u0161\\\3\2\2\2\u0162\u0163\7e\2\2\u0163"+
		"\u0164\7v\2\2\u0164\u0165\7g\2\2\u0165\u0166\7e\2\2\u0166\u0167\7j\2\2"+
		"\u0167^\3\2\2\2\u0168\u0169\7e\2\2\u0169\u016a\7r\2\2\u016a\u016b\7c\2"+
		"\2\u016b\u016c\7t\2\2\u016c\u016d\7o\2\2\u016d`\3\2\2\2\u016e\u016f\7"+
		"e\2\2\u016f\u0170\7u\2\2\u0170\u0171\7r\2\2\u0171\u0172\7c\2\2\u0172\u0173"+
		"\7e\2\2\u0173\u0174\7g\2\2\u0174b\3\2\2\2\u0175\u0176\7u\2\2\u0176\u0177"+
		"\7v\2\2\u0177\u0178\7g\2\2\u0178\u0179\7e\2\2\u0179\u017a\7j\2\2\u017a"+
		"d\3\2\2\2\u017b\u017c\7e\2\2\u017c\u017d\7r\2\2\u017d\u017e\7c\2\2\u017e"+
		"\u017f\7t\2\2\u017f\u0180\7o\2\2\u0180\u0181\7c\2\2\u0181f\3\2\2\2\u0182"+
		"\u0183\7e\2\2\u0183\u0184\7r\2\2\u0184\u0185\7c\2\2\u0185\u0186\7t\2\2"+
		"\u0186\u0187\7o\2\2\u0187\u0188\7d\2\2\u0188h\3\2\2\2\u0189\u018a\5m\67"+
		"\2\u018a\u018b\7\61\2\2\u018b\u018c\5m\67\2\u018cj\3\2\2\2\u018d\u018e"+
		"\5m\67\2\u018e\u0190\7\61\2\2\u018f\u0191\5m\67\2\u0190\u018f\3\2\2\2"+
		"\u0190\u0191\3\2\2\2\u0191\u0192\3\2\2\2\u0192\u0193\7\61\2\2\u0193\u0194"+
		"\5m\67\2\u0194l\3\2\2\2\u0195\u0197\7/\2\2\u0196\u0195\3\2\2\2\u0196\u0197"+
		"\3\2\2\2\u0197\u0199\3\2\2\2\u0198\u019a\5q9\2\u0199\u0198\3\2\2\2\u019a"+
		"\u019b\3\2\2\2\u019b\u0199\3\2\2\2\u019b\u019c\3\2\2\2\u019cn\3\2\2\2"+
		"\u019d\u01a5\5m\67\2\u019e\u01a2\7\60\2\2\u019f\u01a1\5q9\2\u01a0\u019f"+
		"\3\2\2\2\u01a1\u01a4\3\2\2\2\u01a2\u01a0\3\2\2\2\u01a2\u01a3\3\2\2\2\u01a3"+
		"\u01a6\3\2\2\2\u01a4\u01a2\3\2\2\2\u01a5\u019e\3\2\2\2\u01a5\u01a6\3\2"+
		"\2\2\u01a6p\3\2\2\2\u01a7\u01a8\4\62;\2\u01a8r\3\2\2\2\u01a9\u01ad\7%"+
		"\2\2\u01aa\u01ac\5}?\2\u01ab\u01aa\3\2\2\2\u01ac\u01af\3\2\2\2\u01ad\u01ab"+
		"\3\2\2\2\u01ad\u01ae\3\2\2\2\u01ae\u01b2\3\2\2\2\u01af\u01ad\3\2\2\2\u01b0"+
		"\u01b3\5{>\2\u01b1\u01b3\7\2\2\3\u01b2\u01b0\3\2\2\2\u01b2\u01b1\3\2\2"+
		"\2\u01b3\u01b4\3\2\2\2\u01b4\u01b5\b:\2\2\u01b5t\3\2\2\2\u01b6\u01b8\t"+
		"\2\2\2\u01b7\u01b6\3\2\2\2\u01b8\u01b9\3\2\2\2\u01b9\u01b7\3\2\2\2\u01b9"+
		"\u01ba\3\2\2\2\u01bav\3\2\2\2\u01bb\u01bd\n\3\2\2\u01bc\u01bb\3\2\2\2"+
		"\u01bd\u01be\3\2\2\2\u01be\u01bc\3\2\2\2\u01be\u01bf\3\2\2\2\u01bfx\3"+
		"\2\2\2\u01c0\u01c4\t\4\2\2\u01c1\u01c2\7^\2\2\u01c2\u01c4\5{>\2\u01c3"+
		"\u01c0\3\2\2\2\u01c3\u01c1\3\2\2\2\u01c4\u01c5\3\2\2\2\u01c5\u01c3\3\2"+
		"\2\2\u01c5\u01c6\3\2\2\2\u01c6\u01c7\3\2\2\2\u01c7\u01c8\b=\2\2\u01c8"+
		"z\3\2\2\2\u01c9\u01cb\7\17\2\2\u01ca\u01cc\7\f\2\2\u01cb\u01ca\3\2\2\2"+
		"\u01cb\u01cc\3\2\2\2\u01cc\u01cf\3\2\2\2\u01cd\u01cf\7\f\2\2\u01ce\u01c9"+
		"\3\2\2\2\u01ce\u01cd\3\2\2\2\u01cf|\3\2\2\2\u01d0\u01d1\n\5\2\2\u01d1"+
		"~\3\2\2\2\u01d2\u01d4\n\6\2\2\u01d3\u01d2\3\2\2\2\u01d4\u01d5\3\2\2\2"+
		"\u01d5\u01d3\3\2\2\2\u01d5\u01d6\3\2\2\2\u01d6\u0080\3\2\2\2\21\2\u0190"+
		"\u0196\u019b\u01a2\u01a5\u01ad\u01b2\u01b9\u01be\u01c3\u01c5\u01cb\u01ce"+
		"\u01d5\3\b\2\2";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}