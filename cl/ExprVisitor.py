# Generated from Expr.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .ExprParser import ExprParser
else:
    from ExprParser import ExprParser

# This class defines a complete generic visitor for a parse tree produced by ExprParser.

class ExprVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ExprParser#root.
    def visitRoot(self, ctx:ExprParser.RootContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#expr.
    def visitExpr(self, ctx:ExprParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#assignment.
    def visitAssignment(self, ctx:ExprParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#command.
    def visitCommand(self, ctx:ExprParser.CommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#printCommand.
    def visitPrintCommand(self, ctx:ExprParser.PrintCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#areaCommand.
    def visitAreaCommand(self, ctx:ExprParser.AreaCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#perimeterCommand.
    def visitPerimeterCommand(self, ctx:ExprParser.PerimeterCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#verticesCommand.
    def visitVerticesCommand(self, ctx:ExprParser.VerticesCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#centroidCommand.
    def visitCentroidCommand(self, ctx:ExprParser.CentroidCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#colorCommand.
    def visitColorCommand(self, ctx:ExprParser.ColorCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#insideCommand.
    def visitInsideCommand(self, ctx:ExprParser.InsideCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#equalCommand.
    def visitEqualCommand(self, ctx:ExprParser.EqualCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#drawCommand.
    def visitDrawCommand(self, ctx:ExprParser.DrawCommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#operation.
    def visitOperation(self, ctx:ExprParser.OperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#parenthesisOP.
    def visitParenthesisOP(self, ctx:ExprParser.ParenthesisOPContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#boundingBoxOp.
    def visitBoundingBoxOp(self, ctx:ExprParser.BoundingBoxOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#nCreateOp.
    def visitNCreateOp(self, ctx:ExprParser.NCreateOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#variable.
    def visitVariable(self, ctx:ExprParser.VariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#listpoints.
    def visitListpoints(self, ctx:ExprParser.ListpointsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#point.
    def visitPoint(self, ctx:ExprParser.PointContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#real.
    def visitReal(self, ctx:ExprParser.RealContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#rgbColor.
    def visitRgbColor(self, ctx:ExprParser.RgbColorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#listOperations.
    def visitListOperations(self, ctx:ExprParser.ListOperationsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#output.
    def visitOutput(self, ctx:ExprParser.OutputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#string.
    def visitString(self, ctx:ExprParser.StringContext):
        return self.visitChildren(ctx)



del ExprParser