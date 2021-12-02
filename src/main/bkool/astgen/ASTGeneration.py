from BKOOLVisitor import BKOOLVisitor
from BKOOLParser import BKOOLParser
from AST import *

# from initial.src.main.bkool.utils.AST import *

class ASTGeneration(BKOOLVisitor):

    def visitProgram(self, ctx:BKOOLParser.ProgramContext):
        return Program([self.visit(x) for x in ctx.classdecl()])

    def visitClassdecl(self, ctx:BKOOLParser.ClassdeclContext):
        if ctx.EXTENDS():
            return ClassDecl(Id(ctx.ID(0).getText()), self.visit(ctx.memberlist()), Id(ctx.ID(1).getText()))
        else:
            return ClassDecl(Id(ctx.ID(0).getText()), self.visit(ctx.memberlist()))

    '''Return [AttributeDecl, MethodDecl, ...]'''
    def visitMemberlist(self, ctx:BKOOLParser.MemberlistContext):
        if ctx.attribute():
            return self.visit(ctx.attribute()) + self.visit(ctx.memberlist())
        elif ctx.method():
            return self.visit(ctx.method()) + self.visit(ctx.memberlist())
        else: return []

    '''Return [AttributeDecl(Static(), VarDecl()), AttributeDecl(Instance(), ConstDecl())]'''
    def visitAttribute(self, ctx:BKOOLParser.AttributeContext):
        if ctx.STATIC():
            if ctx.FINAL():
                typekeyword = self.visit(ctx.typekeyword())
                initials = self.visit(ctx.initials())
                
                constDecl = [ConstDecl(x[0], typekeyword, x[1]) for x in initials]

                return [AttributeDecl(Static(), x) for x in constDecl]
            else:
                return [AttributeDecl(Static(), x) for x in self.visit(ctx.storedecl())]
        else:
            return [AttributeDecl(Instance(), x) for x in self.visit(ctx.storedecl())]

    def visitStoredecl(self, ctx:BKOOLParser.StoredeclContext):
        if ctx.vardecl():
            return self.visit(ctx.vardecl())
        if ctx.constdecl():
            return self.visit(ctx.constdecl())

    '''Return [VarDecl(Id, Type, Expr), VarDecl(Id, Type, Expr), ...]'''
    def visitVardecl(self, ctx:BKOOLParser.VardeclContext):
        typekeyword = self.visit(ctx.typekeyword())
        initials = self.visit(ctx.initials())

        return [VarDecl(x[0], typekeyword, x[1]) for x in initials]

    '''Return [ConstDecl(Id, Type, Expr), ConstDecl(Id, Type, Expr), ...]'''
    def visitConstdecl(self, ctx:BKOOLParser.ConstdeclContext):
        typekeyword = self.visit(ctx.typekeyword())
        initials = self.visit(ctx.initials())

        return [ConstDecl(x[0], typekeyword, x[1]) for x in initials]

    '''Return [(ID, expr), (ID, None)]'''
    def visitInitials(self, ctx:BKOOLParser.InitialsContext):
        if ctx.exp():
            if ctx.initials():
                return [(Id(ctx.ID().getText()), self.visit(ctx.exp()))] + self.visit(ctx.initials())
            else:
                return [(Id(ctx.ID().getText()), self.visit(ctx.exp()))]
        else:
            if ctx.initials():
                return [(Id(ctx.ID().getText()), None)] + self.visit(ctx.initials())
            else:
                return [(Id(ctx.ID().getText()), None)]

    '''Return MethodDecl(SIKind, Id, [VarDecl], Type, Block)'''
    def visitMethod(self, ctx:BKOOLParser.MethodContext):
        varDecl = []

        if ctx.paramlist():
            varDecl = self.visit(ctx.paramlist())

        if ctx.STATIC():
            if ctx.typekeyword():
                return [MethodDecl(Static(), Id(ctx.ID().getText()), varDecl, self.visit(ctx.typekeyword()), self.visit(ctx.blockstatement()))]
            else:
                return [MethodDecl(Static(), Id(ctx.ID().getText()), varDecl, VoidType(), self.visit(ctx.blockstatement()))]
        else:
            if ctx.typekeyword():
                return [MethodDecl(Instance(), Id(ctx.ID().getText()), varDecl, self.visit(ctx.typekeyword()), self.visit(ctx.blockstatement()))]
            elif ctx.VOIDTYPE():
                return [MethodDecl(Instance(), Id(ctx.ID().getText()), varDecl, VoidType(), self.visit(ctx.blockstatement()))]
            else:
                return [MethodDecl(Instance(), Id("<init>"), varDecl, None, self.visit(ctx.blockstatement()))]

    '''Return [VarDecl(Id, Type, Expr), VarDecl(Id, Type, Expr), ...]'''
    def visitParamlist(self, ctx:BKOOLParser.ParamlistContext):
        if ctx.paramlist():
            return self.visit(ctx.paramdecl()) + self.visit(ctx.paramlist())
        else: return self.visit(ctx.paramdecl())

    '''Return [VarDecl(Id, Type, Expr), VarDecl(Id, Type, Expr), ...]'''
    def visitParamdecl(self, ctx:BKOOLParser.ParamdeclContext):
        return list(map(lambda x: VarDecl(x, self.visit(ctx.typekeyword())), self.visit(ctx.idlist())))

    '''Return [Id, Id, ...]'''
    def visitIdlist(self, ctx:BKOOLParser.IdlistContext):
        if ctx.idlist():
            return [Id(ctx.ID().getText())] + self.visit(ctx.idlist())
        else:
            return [Id(ctx.ID().getText())]

    '''Return 1 Type (IntType, FloatType, BoolType, StringType, ArrayType, ClassType)'''
    def visitTypekeyword(self, ctx:BKOOLParser.TypekeywordContext):
        if ctx.BOOLEANTYPE(): return BoolType()
        elif ctx.INTTYPE(): return IntType()
        elif ctx.FLOATTYPE(): return FloatType()
        elif ctx.STRINGTYPE(): return StringType()
        elif ctx.ID():
            return ClassType(Id(ctx.ID().getText()))
        elif ctx.arraytype():
            return self.visit(ctx.arraytype())

    '''Return ArrayType(int, Type)'''
    def visitArraytype(self, ctx:BKOOLParser.ArraytypeContext):
        eleType = None

        if ctx.BOOLEANTYPE(): eleType = BoolType()
        elif ctx.INTTYPE(): eleType = IntType()
        elif ctx.FLOATTYPE(): eleType = FloatType()
        elif ctx.STRINGTYPE(): eleType = StringType()
        elif ctx.ID():
            eleType = ClassType(Id(ctx.ID().getText()))
        
        return ArrayType(int(ctx.INTLIT().getText()), eleType)

    '''Return Assign || Break || ...'''
    def visitStatement(self, ctx:BKOOLParser.StatementContext):
        if ctx.assignment():
            return self.visit(ctx.assignment())
        if ctx.breakstmt():
            return self.visit(ctx.breakstmt())
        if ctx.continuestmt():
            return self.visit(ctx.continuestmt())
        if ctx.ret():
            return self.visit(ctx.ret())
        if ctx.callstmt():
            return self.visit(ctx.callstmt())
        if ctx.ifstmt():
            return self.visit(ctx.ifstmt())
        if ctx.forstmt():
            return self.visit(ctx.forstmt())
        if ctx.blockstatement():
            return self.visit(ctx.blockstatement())

    '''Return Assign(Expr, Expr)'''
    def visitAssignment(self, ctx:BKOOLParser.AssignmentContext):
        return Assign(self.visit(ctx.lhs()), self.visit(ctx.exp()))

    '''Return Id || ArrayCell(Expr, Expr) || FieldAccess(Expr, Id)'''
    def visitLhs(self, ctx:BKOOLParser.LhsContext):
        if ctx.ID():
            return Id(ctx.ID().getText())
        if ctx.exparray():
            return self.visit(ctx.exparray())
        if ctx.fieldaccess():
            return self.visit(ctx.fieldaccess())

    '''Return If(Expr, Stmt, Stmt = None)'''
    def visitIfstmt(self, ctx:BKOOLParser.IfstmtContext):
        exp = self.visit(ctx.exp())

        if ctx.ELSE():
            return If(exp, self.visit(ctx.statement(0)), self.visit(ctx.statement(1)))
        else:
            return If(exp, self.visit(ctx.statement(0)))

    '''Return For(Id, Expr, Expr, bool, Stmt || Block)'''
    def visitForstmt(self, ctx:BKOOLParser.ForstmtContext):
        expr1 = self.visit(ctx.exp(0))
        expr2 = self.visit(ctx.exp(1))

        if ctx.TO():
            return For(Id(ctx.ID().getText()), expr1, expr2, True, self.visit(ctx.statement()))
        else:
            return For(Id(ctx.ID().getText()), expr1, expr2, False, self.visit(ctx.statement()))

    '''Return Block([VarDecl, ConstDecl, ...], [Stmt, Stmt, ...])'''
    def visitBlockstatement(self, ctx:BKOOLParser.BlockstatementContext):
        return Block(self.visit(ctx.storedecls()), self.visit(ctx.statements()))

    def visitStoredecls(self, ctx:BKOOLParser.StoredeclsContext):
        if ctx.storedecl():
            return self.visit(ctx.storedecl()) + self.visit(ctx.storedecls())
        else:
            return []

    '''Return [Stmt]'''
    def visitStatements(self, ctx:BKOOLParser.StatementsContext):
        if ctx.statement():
            return [self.visit(ctx.statement())] + self.visit(ctx.statements())
        else:
            return []

    '''Return CallStmt(Expr, Id, [Expr])'''
    def visitCallstmt(self, ctx:BKOOLParser.CallstmtContext):
        if ctx.arglist():
            return CallStmt(self.visit(ctx.expcall()), Id(ctx.ID().getText()), self.visit(ctx.arglist()))
        else:
            return CallStmt(self.visit(ctx.expcall()), Id(ctx.ID().getText()), [])
    
    '''Return [Expr, Expr, ...]'''
    def visitArglist(self, ctx:BKOOLParser.ArglistContext):
        if ctx.arglist():
            return [self.visit(ctx.exp())] + self.visit(ctx.arglist())
        else:
            return [self.visit(ctx.exp())]

    def visitContinuestmt(self, ctx:BKOOLParser.ContinuestmtContext):
        return Continue()
    def visitBreakstmt(self, ctx:BKOOLParser.BreakstmtContext):
        return Break()

    '''Return Return(Expr)'''
    def visitRet(self, ctx:BKOOLParser.RetContext):
        return Return(self.visit(ctx.exp()))

    '''Return Expr'''
    def visitExp(self, ctx:BKOOLParser.ExpContext):
        if ctx.GT():
            return BinaryOp('>', self.visit(ctx.expnoneay(0)), self.visit(ctx.expnoneay(1)))
        elif ctx.LT():
            return BinaryOp('<', self.visit(ctx.expnoneay(0)), self.visit(ctx.expnoneay(1)))
        elif ctx.GTOE():
            return BinaryOp('>=', self.visit(ctx.expnoneay(0)), self.visit(ctx.expnoneay(1)))
        elif ctx.LTOE():
            return BinaryOp('<=', self.visit(ctx.expnoneay(0)), self.visit(ctx.expnoneay(1)))
        else:
            return self.visit(ctx.expnoneay(0))

    def visitExpnoneay(self, ctx:BKOOLParser.ExpnoneayContext):
        if ctx.EQUAL():
            return BinaryOp('==', self.visit(ctx.explogic(0)), self.visit(ctx.explogic(1)))
        elif ctx.NOTEQUAL():
            return BinaryOp('!=', self.visit(ctx.explogic(0)), self.visit(ctx.explogic(1)))
        else:
            return self.visit(ctx.explogic(0))

    def visitExplogic(self, ctx:BKOOLParser.ExplogicContext):
        if ctx.AND():
            return BinaryOp('&&', self.visit(ctx.explogic()), self.visit(ctx.exp1()))
        elif ctx.OR():
            return BinaryOp('||', self.visit(ctx.explogic()), self.visit(ctx.exp1()))
        else:
            return self.visit(ctx.exp1())

    def visitExp1(self, ctx:BKOOLParser.Exp1Context):
        if ctx.ADD():
            return BinaryOp('+', self.visit(ctx.exp1()), self.visit(ctx.exp2()))
        elif ctx.SUB():
            return BinaryOp('-', self.visit(ctx.exp1()), self.visit(ctx.exp2()))
        else:
            return self.visit(ctx.exp2())

    def visitExp2(self, ctx:BKOOLParser.Exp2Context):
        if ctx.MUL():
            return BinaryOp('*', self.visit(ctx.exp2()), self.visit(ctx.expstring()))
        elif ctx.DIVFLOAT():
            return BinaryOp('/', self.visit(ctx.exp2()), self.visit(ctx.expstring()))
        elif ctx.DIVINT():
            return BinaryOp('\\', self.visit(ctx.exp2()), self.visit(ctx.expstring()))
        elif ctx.MOD():
            return BinaryOp('%', self.visit(ctx.exp2()), self.visit(ctx.expstring()))
        else:
            return self.visit(ctx.expstring())

    def visitExpstring(self, ctx:BKOOLParser.ExpstringContext):
        if ctx.CONCAT():
            return BinaryOp('^', self.visit(ctx.expstring()), self.visit(ctx.expnot()))
        else:
            return self.visit(ctx.expnot())

    '''Return Unary('!', Expr) || Expnot'''
    def visitExpnot(self, ctx:BKOOLParser.ExpnotContext):
        if ctx.NOT():
            return UnaryOp('!', self.visit(ctx.expnot()))
        else:
            return self.visit(ctx.expsign())

    '''Return Unary('+', Expr) || Unary('-', Expr) || Exparray'''
    def visitExpsign(self, ctx:BKOOLParser.ExpsignContext):
        if ctx.ADD():
            return UnaryOp('+', self.visit(ctx.expsign()))
        elif ctx.SUB():
            return UnaryOp('-', self.visit(ctx.expsign()))
        else:
            return self.visit(ctx.exparray())

    '''Return ArrayCell(Expr, Expr) || Expcall'''
    def visitExparray(self, ctx:BKOOLParser.ExparrayContext):
        if ctx.exp():
            return ArrayCell(self.visit(ctx.expcall()), self.visit(ctx.exp()))
        else:
            return self.visit(ctx.expcall())

    '''Return CallExpr()'''
    def visitExpcall(self, ctx:BKOOLParser.ExpcallContext):
        if ctx.expcall():
            if ctx.LB():
                argList = []
                if ctx.arglist():
                    argList = self.visit(ctx.arglist())

                return CallExpr(self.visit(ctx.expcall()), Id(ctx.ID().getText()), argList)
            else:
                return FieldAccess(self.visit(ctx.expcall()), Id(ctx.ID().getText()))
        else:
            return self.visit(ctx.expnew())

    def visitExpnew(self, ctx:BKOOLParser.ExpnewContext):
        if ctx.NEW():
            argList = []

            if ctx.arglist():
                argList = self.visit(ctx.arglist())

            return NewExpr(Id(ctx.ID().getText()), argList)
        elif ctx.exp():
            return self.visit(ctx.exp())
        else:
            return self.visit(ctx.term())

    '''Return (Not a list)'''
    def visitTerm(self, ctx:BKOOLParser.TermContext):
        if ctx.INTLIT():
            return IntLiteral(int(ctx.INTLIT().getText()))
        elif ctx.FLOATLIT():
            return FloatLiteral(float(ctx.FLOATLIT().getText()))
        elif ctx.TRUE():
            return BooleanLiteral(True)
        elif ctx.FALSE():
            return BooleanLiteral(False)
        elif ctx.STRINGLITS():
            return StringLiteral(ctx.STRINGLITS().getText())
        elif ctx.arraylits():
            return ArrayLiteral(self.visit(ctx.arraylits()))
        elif ctx.NIL():
            return NullLiteral()
        elif ctx.THIS():
            return SelfLiteral()
        else:
            return Id(ctx.ID().getText())

    def visitArraylits(self, ctx:BKOOLParser.ArraylitsContext):
        # if ctx.arrayintlits():
        #     return self.visit(ctx.arrayintlits())
        # elif ctx.arrayfloatlits():
        #     return self.visit(ctx.arrayfloatlits())
        # elif ctx.arraybooleanlits():
        #     return self.visit(ctx.arraybooleanlits())
        # else:
        #     return self.visit(ctx.arraystringlits())
        if ctx.COMMA():
            return self.visit(ctx.arrayelelits()) + self.visit(ctx.arraylits())
        else:
            return self.visit(ctx.arrayelelits())

    '''Return [Literals with the same type or not ????]'''
    def visitArrayelelits(self, ctx:BKOOLParser.ArrayelelitsContext):
        if ctx.INTLIT():
            return [IntLiteral(int(ctx.INTLIT().getText()))]
        elif ctx.FLOATLIT():
            return [FloatLiteral(float(ctx.FLOATLIT().getText()))]
        elif ctx.TRUE():
            return [BooleanLiteral(True)]
        elif ctx.FALSE():
            return [BooleanLiteral(False)]
        else:
            return [StringLiteral(ctx.STRINGLITS().getText())]
    # def visitArrayintlits(self, ctx:BKOOLParser.ArrayintlitsContext):
    #     if ctx.COMMA():
    #         return [IntLiteral(int(ctx.INTLIT().getText()))] + self.visit(ctx.arrayintlits())
    #     else:
    #         return [IntLiteral(int(ctx.INTLIT().getText()))]
    # def visitArrayfloatlits(self, ctx:BKOOLParser.ArrayfloatlitsContext):
    #     if ctx.COMMA():
    #         return [FloatLiteral(float(ctx.FLOATLIT().getText()))] + self.visit(ctx.arrayfloatlits())
    #     else:
    #         return [FloatLiteral(float(ctx.FLOATLIT().getText()))]
    # def visitArraybooleanlits(self, ctx:BKOOLParser.ArraybooleanlitsContext):
    #     if ctx.COMMA():
    #         if ctx.TRUE():
    #             return [BooleanLiteral(True)] + self.visit(ctx.arraybooleanlits())
    #         else:
    #             return [BooleanLiteral(False)] + self.visit(ctx.arraybooleanlits())
    #     else:
    #         if ctx.TRUE():
    #             return [BooleanLiteral(True)]
    #         else:
    #             return [BooleanLiteral(False)]
    # def visitArraystringlits(self, ctx:BKOOLParser.ArraystringlitsContext):
    #     if ctx.COMMA():
    #         return [StringLiteral(ctx.STRINGLITS().getText())] + self.visit(ctx.arraystringlits())
    #     else:
    #         return [StringLiteral(ctx.STRINGLITS().getText())]