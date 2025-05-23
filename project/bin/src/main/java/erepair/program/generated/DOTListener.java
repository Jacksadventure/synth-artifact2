// Generated from DOT.g4 by ANTLR 4.9.2
package erepair.program.generated;
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link DOTParser}.
 */
public interface DOTListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link DOTParser#graph}.
	 * @param ctx the parse tree
	 */
	void enterGraph(DOTParser.GraphContext ctx);
	/**
	 * Exit a parse tree produced by {@link DOTParser#graph}.
	 * @param ctx the parse tree
	 */
	void exitGraph(DOTParser.GraphContext ctx);
	/**
	 * Enter a parse tree produced by {@link DOTParser#stmt_list}.
	 * @param ctx the parse tree
	 */
	void enterStmt_list(DOTParser.Stmt_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link DOTParser#stmt_list}.
	 * @param ctx the parse tree
	 */
	void exitStmt_list(DOTParser.Stmt_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link DOTParser#stmt}.
	 * @param ctx the parse tree
	 */
	void enterStmt(DOTParser.StmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link DOTParser#stmt}.
	 * @param ctx the parse tree
	 */
	void exitStmt(DOTParser.StmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link DOTParser#attr_stmt}.
	 * @param ctx the parse tree
	 */
	void enterAttr_stmt(DOTParser.Attr_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link DOTParser#attr_stmt}.
	 * @param ctx the parse tree
	 */
	void exitAttr_stmt(DOTParser.Attr_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link DOTParser#attr_list}.
	 * @param ctx the parse tree
	 */
	void enterAttr_list(DOTParser.Attr_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link DOTParser#attr_list}.
	 * @param ctx the parse tree
	 */
	void exitAttr_list(DOTParser.Attr_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link DOTParser#a_list}.
	 * @param ctx the parse tree
	 */
	void enterA_list(DOTParser.A_listContext ctx);
	/**
	 * Exit a parse tree produced by {@link DOTParser#a_list}.
	 * @param ctx the parse tree
	 */
	void exitA_list(DOTParser.A_listContext ctx);
	/**
	 * Enter a parse tree produced by {@link DOTParser#edge_stmt}.
	 * @param ctx the parse tree
	 */
	void enterEdge_stmt(DOTParser.Edge_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link DOTParser#edge_stmt}.
	 * @param ctx the parse tree
	 */
	void exitEdge_stmt(DOTParser.Edge_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link DOTParser#edgeRHS}.
	 * @param ctx the parse tree
	 */
	void enterEdgeRHS(DOTParser.EdgeRHSContext ctx);
	/**
	 * Exit a parse tree produced by {@link DOTParser#edgeRHS}.
	 * @param ctx the parse tree
	 */
	void exitEdgeRHS(DOTParser.EdgeRHSContext ctx);
	/**
	 * Enter a parse tree produced by {@link DOTParser#edgeop}.
	 * @param ctx the parse tree
	 */
	void enterEdgeop(DOTParser.EdgeopContext ctx);
	/**
	 * Exit a parse tree produced by {@link DOTParser#edgeop}.
	 * @param ctx the parse tree
	 */
	void exitEdgeop(DOTParser.EdgeopContext ctx);
	/**
	 * Enter a parse tree produced by {@link DOTParser#node_stmt}.
	 * @param ctx the parse tree
	 */
	void enterNode_stmt(DOTParser.Node_stmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link DOTParser#node_stmt}.
	 * @param ctx the parse tree
	 */
	void exitNode_stmt(DOTParser.Node_stmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link DOTParser#node_id}.
	 * @param ctx the parse tree
	 */
	void enterNode_id(DOTParser.Node_idContext ctx);
	/**
	 * Exit a parse tree produced by {@link DOTParser#node_id}.
	 * @param ctx the parse tree
	 */
	void exitNode_id(DOTParser.Node_idContext ctx);
	/**
	 * Enter a parse tree produced by {@link DOTParser#port}.
	 * @param ctx the parse tree
	 */
	void enterPort(DOTParser.PortContext ctx);
	/**
	 * Exit a parse tree produced by {@link DOTParser#port}.
	 * @param ctx the parse tree
	 */
	void exitPort(DOTParser.PortContext ctx);
	/**
	 * Enter a parse tree produced by {@link DOTParser#subgraph}.
	 * @param ctx the parse tree
	 */
	void enterSubgraph(DOTParser.SubgraphContext ctx);
	/**
	 * Exit a parse tree produced by {@link DOTParser#subgraph}.
	 * @param ctx the parse tree
	 */
	void exitSubgraph(DOTParser.SubgraphContext ctx);
	/**
	 * Enter a parse tree produced by {@link DOTParser#id_}.
	 * @param ctx the parse tree
	 */
	void enterId_(DOTParser.Id_Context ctx);
	/**
	 * Exit a parse tree produced by {@link DOTParser#id_}.
	 * @param ctx the parse tree
	 */
	void exitId_(DOTParser.Id_Context ctx);
}