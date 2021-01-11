if __name__ is not None and "." in __name__:
    from .ExprParser import ExprParser
    from .ExprVisitor import ExprVisitor
else:
    from ExprParser import ExprParser
    from ExprVisitor import ExprVisitor

import random
import sys
sys.path.append("..")
from polygons import ConvexPolygon

class EvalVisitor(ExprVisitor):

    def __init__(self):
        self.dic = {}
    
    # Visit a parse tree produced by ExprParser#root.
    def visitRoot(self, ctx:ExprParser.RootContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#expr.
    def visitExpr(self, ctx:ExprParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#assignment.
    def visitAssignment(self, ctx:ExprParser.AssignmentContext):
        l = [n for n in ctx.getChildren()]
        self.dic[l[0].getText()] = self.visit(l[2])


    # Visit a parse tree produced by ExprParser#command.
    def visitCommand(self, ctx:ExprParser.CommandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ExprParser#printCommand.
    def visitPrintCommand(self, ctx:ExprParser.PrintCommandContext):
        l = [n for n in ctx.getChildren()]
        print (self.visit(l[1]))


    # Visit a parse tree produced by ExprParser#areaCommand.
    def visitAreaCommand(self, ctx:ExprParser.AreaCommandContext):
        l = [n for n in ctx.getChildren()]
        print ("%.3f" % self.visit(l[1]).get_area())


    # Visit a parse tree produced by ExprParser#perimeterCommand.
    def visitPerimeterCommand(self, ctx:ExprParser.PerimeterCommandContext):
        l = [n for n in ctx.getChildren()]
        print ("%.3f" % self.visit(l[1]).get_perimeter())


    # Visit a parse tree produced by ExprParser#verticesCommand.
    def visitVerticesCommand(self, ctx:ExprParser.VerticesCommandContext):
        l = [n for n in ctx.getChildren()]
        print (self.visit(l[1]).get_n_vertices())


    # Visit a parse tree produced by ExprParser#centroidCommand.
    def visitCentroidCommand(self, ctx:ExprParser.CentroidCommandContext):
        l = [n for n in ctx.getChildren()]
        p = self.visit(l[1]).get_centroid()
        print ("%.3f %.3f" % (p[0], p[1]))


    # Visit a parse tree produced by ExprParser#colorCommand.
    def visitColorCommand(self, ctx:ExprParser.ColorCommandContext):
        l = [n for n in ctx.getChildren()]
        self.dic[l[1].getText()].set_color(self.visit(l[3]))


    # Visit a parse tree produced by ExprParser#insideCommand.
    def visitInsideCommand(self, ctx:ExprParser.InsideCommandContext):
        l = [n for n in ctx.getChildren()]
        if self.visit(l[3]).is_polygon_inside(self.visit(l[1])) == True:
            print("Yes")
        else: 
            print ("No")


    # Visit a parse tree produced by ExprParser#equalCommand.
    def visitEqualCommand(self, ctx:ExprParser.EqualCommandContext):
        l = [n for n in ctx.getChildren()]
        if self.visit(l[3]).is_equal(self.visit(l[1])) == True:
            print("Yes")
        else: 
            print ("No")


    # Visit a parse tree produced by ExprParser#drawCommand.
    def visitDrawCommand(self, ctx:ExprParser.DrawCommandContext):
        l = [n for n in ctx.getChildren()]
        list_P = self.visit(l[3])
        output = self.visit(l[1])
        ConvexPolygon.draw(list_P, output)


    # Visit a parse tree produced by ExprParser#operation.
    def visitOperation(self, ctx:ExprParser.OperationContext):
        l = [n for n in ctx.getChildren()]        
        if len(l) == 1:
            return self.visitChildren(ctx)
        elif len(l) == 3:
            if l[1].getText() == '+':
                return ConvexPolygon.convex_union([self.visit(l[0]), self.visit(l[2])])
            else:
                return ConvexPolygon.convex_union([self.visit(l[0]), self.visit(l[2])])


    # Visit a parse tree produced by ExprParser#parenthesisOP.
    def visitParenthesisOP(self, ctx:ExprParser.ParenthesisOPContext):
        l = [n for n in ctx.getChildren()]
        return self.visit(l[1])


    # Visit a parse tree produced by ExprParser#boundingBoxOp.
    def visitBoundingBoxOp(self, ctx:ExprParser.BoundingBoxOpContext):
        l = [n for n in ctx.getChildren()]
        return ConvexPolygon.bounding_box([self.visit(l[1])])


    # Visit a parse tree produced by ExprParser#nCreateOp.
    def visitNCreateOp(self, ctx:ExprParser.NCreateOpContext):
        l = [n for n in ctx.getChildren()]
        num = int(self.visit(l[1]))
        randomlist = [(random.uniform(0, 1), random.uniform(0, 1)) for i in range(num)]
        return ConvexPolygon(randomlist)

    # Visit a parse tree produced by ExprParser#variable.
    def visitVariable(self, ctx:ExprParser.VariableContext):
        name = next(ctx.getChildren()).getText()
        return self.dic[name]


    # Visit a parse tree produced by ExprParser#listpoints.
    def visitListpoints(self, ctx:ExprParser.ListpointsContext):
        l = [n for n in ctx.getChildren()]
        l.pop(0)
        l.pop(-1)
        points = [self.visit(c) for c in l]
        return ConvexPolygon(points)


    # Visit a parse tree produced by ExprParser#point.
    def visitPoint(self, ctx:ExprParser.PointContext):
        l = [n for n in ctx.getChildren()]
        return (self.visit(l[0]), self.visit(l[1]))


    # Visit a parse tree produced by ExprParser#real.
    def visitReal(self, ctx:ExprParser.RealContext):
        return float(next(ctx.getChildren()).getText())


    # Visit a parse tree produced by ExprParser#rgbColor.
    def visitRgbColor(self, ctx:ExprParser.RgbColorContext):
        l = [n for n in ctx.getChildren()]
        return (self.visit(l[1]), self.visit(l[2]), self.visit(l[3]))


    # Visit a parse tree produced by ExprParser#listOperations.
    def visitListOperations(self, ctx:ExprParser.ListOperationsContext):
        l = [n for n in ctx.getChildren()]
        listOp = []
        for elem in l[::2]:
            listOp.append(self.visit(elem))
        return listOp


    # Visit a parse tree produced by ExprParser#output.
    def visitOutput(self, ctx:ExprParser.OutputContext):
        s = next(ctx.getChildren()).getText()
        return s[1:-1]


    # Visit a parse tree produced by ExprParser#string.
    def visitString(self, ctx:ExprParser.StringContext):
        s = next(ctx.getChildren()).getText()
        return s[1:-1]



del ExprParser