/* AST node diagram generator script collection for M2C, M2J and M2Sharp.
 *
 * Copyright (c) 2016 The Modula-2 Software Foundation
 *
 * Author & Maintainer: Benjamin Kowarsch <org.m2sf>
 *
 * @synopsis
 *
 * The M2C, M2J and M2Sharp compilers are multi-dialect Modula-2 translators
 * and compilers respectively targeting C99, Java/JVM and C#/CLR, sharing a
 * common abstract syntax tree (AST) specification.
 *
 * The AST node diagram generator script collection consists of Graphviz DOT
 * descriptions for all AST node types of the common AST specification.
 *
 * The Graphviz dot utility is required to generate the diagrams. 
 * It may be obtained from http://www.graphviz.org/download.php.
 *
 * @repository
 *
 * https://github.com/m2sf/m2-ast-node-diagrams
 *
 * @file
 *
 * constdef.dot
 *
 * CONSTDEF node diagram.
 *
 * Usage: $ dot constdef.dot -Tps > constdef.ps
 *
 * @license
 *
 * This is free software: you can redistribute and/or modify it under the
 * terms of the GNU Lesser General Public License (LGPL) either version 2.1
 * or at your choice version 3 as published by the Free Software Foundation.
 * However, you may not alter the copyright, author and license information.
 *
 * It is distributed in the hope that it will be useful,  but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE.  Read the license for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License.
 * If not, see <https://www.gnu.org/copyleft/lesser.html>.
 *
 * NB: Components in the domain part of email addresses are in reverse order.
 */

/*** CONSTDEF Node ***/

digraph CONSTDEF {
  graph [orientation=landscape,fontname=helvetica];
  node [fontname=helvetica,fontsize=10,shape=box,height=0.25];
  
  node [style=solid];
  edge [arrowhead=normal];
  CONSTDEF 0> { id0 id1 };
  id0 [label="IDENT"];
  id1 [label="expr",style=rounded];
  
  id0 -> constIdent;
  constIdent [style=filled,fillcolor=lightgrey];
}

/* END OF FILE */