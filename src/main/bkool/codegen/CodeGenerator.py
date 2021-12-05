from functools import reduce

from Frame import Frame
from abc import ABC
from Visitor import * 
from AST import *

# from src.main.bkool.utils.AST import *;

class MType:
    def __init__(self,partype,rettype):
        self.partype = partype
        self.rettype = rettype

class Symbol:
    def __init__(self,name,mtype,value = None):
        self.name = name
        self.mtype = mtype
        self.value = value
    def __str__(self):
        return "Symbol("+self.name+","+str(self.mtype)+")"

from Emitter import Emitter

class CodeGenerator:
    def __init__(self):
        self.libName = "io"

    def init(self):
        return [
            Symbol("readInt", MType(list(), IntType()), CName(self.libName)),
            Symbol("writeInt", MType([IntType()], VoidType()), CName(self.libName)),
            Symbol("writeIntLn", MType([IntType()], VoidType()), CName(self.libName)),
            Symbol("readFloat", MType(list(), FloatType()), CName(self.libName)),
            Symbol("writeFloat", MType([FloatType()], VoidType()), CName(self.libName)),
            Symbol("writeFloatLn", MType([FloatType()], VoidType()), CName(self.libName)),
            Symbol("readBool", MType(list(), BoolType()), CName(self.libName)),
            Symbol("writeBool", MType([BoolType()], VoidType()), CName(self.libName)),
            Symbol("writeBoolLn", MType([BoolType()], VoidType()), CName(self.libName)),
            Symbol("readStr", MType(list(), StringType()), CName(self.libName)),
            Symbol("writeStr", MType([StringType()], VoidType()), CName(self.libName)),
            Symbol("writeStrLn", MType([StringType()], VoidType()), CName(self.libName)),
        ]

    def gen(self, ast,path):
        #ast: AST
        #dir_: String

        gl = self.init()
        gc = CodeGenVisitor(ast, gl,path)
        gc.visit(ast, None)



class SubBody():
    def __init__(self, frame, sym):
        self.frame = frame
        self.sym = sym

class Access():
    def __init__(self, frame, sym, isLeft, isFirst = False):
        self.frame = frame
        self.sym = sym
        self.isLeft = isLeft
        self.isFirst = isFirst

class Val(ABC):
    pass

class Index(Val):
    def __init__(self, value):
        self.value = value

class CName(Val):
    def __init__(self, value):
        self.value = value

class CodeGenVisitor(BaseVisitor):
    def __init__(self, astTree, env,path):
        self.astTree = astTree
        self.env = env
        self.path = path

    def visitProgram(self, ast, c):
        [self.visit(i, c) for i in ast.decl]
        return c

    def visitClassDecl(self, ast: ClassDecl, c):
        self.className = ast.classname.name
        self.emit = Emitter(self.path+"/" + self.className + ".j")
        
        self.parentName = ast.parentname if ast.parentname else "java.lang.Object"
        self.emit.printout(self.emit.emitPROLOG(self.className, self.parentName))
        
        [self.visit(ele, SubBody(None, self.env)) for ele in ast.memlist if type(ele) == AttributeDecl]
        [self.visit(ele, SubBody(None, self.env)) for ele in ast.memlist if type(ele) == MethodDecl]
        
        # generate default constructor
        self.genMETHOD(MethodDecl(Instance(),Id("<init>"), list(), None, Block([],[])), self.env, Frame("<init>", VoidType()))
        self.emit.emitEPILOG()
        return c
    
    def visitAttributeDecl(self, ast: AttributeDecl, o: SubBody):
        o.frame = ast.kind
        return self.visit(ast.decl, o)
    
    def visitVarDecl(self, ast: VarDecl, o):
        if type(o.frame) is Static:
            code = self.emit.emitSTATICFIELD(ast.variable.name, ast.varType, False)
            self.emit.printout(code)
            return Symbol(ast.variable.name, ast.varType, CName(self.className))
        elif type(o.frame) is Instance:
            code = self.emit.emitINSTANCEFIELD(ast.variable.name, ast.varType)
            self.emit.printout(code)
            return Symbol(ast.variable.name, ast.varType, CName(self.className))
        else:
            idx = o.frame.getNewIndex()
            code = self.emit.emitVAR(idx, ast.variable.name, ast.varType, o.frame.getStartLabel(), o.frame.getEndLabel(), o.frame)
            self.emit.printout(code)
            if ast.varInit:
                initCode, initType = self.visit(ast.varInit, Access(o.frame, o.sym, False))
                self.emit.printout(initCode)
                lhsCode, lhsType = self.visit(ast.variable, Access(o.frame, [Symbol(ast.variable.name, ast.varType, Index(idx))], True, True))
                self.emit.printout(lhsCode)
            return Symbol(ast.variable.name, ast.varType, Index(idx))
    
    def visitConstDecl(self, ast: ConstDecl, o):
        if type(o.frame) is Static:
            code = self.emit.emitSTATICFIELD(ast.constant.name, ast.constType, True)
            self.emit.printout(code)
            return Symbol(ast.constant.name, ast.constType, CName(self.className))
        else:
            idx = o.frame.getNewIndex()
            code = self.emit.emitVAR(idx, ast.constant.name, ast.constType, o.frame.getStartLabel(), o.frame.getEndLabel(), o.frame)
            self.emit.printout(code)
            
            # handle for initial value
            initCode, initType = self.visit(ast.value, Access(o.frame, o.sym, False))
            self.emit.printout(initCode)
            lhsCode, lhsType = self.visit(ast.constant, Access(o.frame, [Symbol(ast.constant.name, ast.constType, Index(idx))], True, True))
            self.emit.printout(lhsCode)
            return Symbol(ast.constant.name, ast.constType, Index(idx))

    def genMETHOD(self, consdecl: MethodDecl, sym, frame):
        isInit = consdecl.returnType is None
        isStatic = not isInit and type(consdecl.kind) is Static
        isMain = consdecl.name.name == "main" and len(consdecl.param) == 0 and type(consdecl.returnType) is VoidType
        returnType = VoidType() if isInit else consdecl.returnType
        methodName = "<init>" if isInit else consdecl.name.name
        intype = [ArrayType(0, StringType())] if isMain else list(map(lambda x: x.varType, consdecl.param))
        mtype = MType(intype, returnType)

        self.emit.printout(self.emit.emitMETHOD(methodName, mtype, isStatic,frame))

        frame.enterScope(True)

        # Generate code for parameter declarations
        local = SubBody(frame, sym)
        if isInit:
            self.emit.printout(self.emit.emitVAR(frame.getNewIndex(), "this", ClassType(Id(self.className)), frame.getStartLabel(), frame.getEndLabel(), frame))
        elif isMain:
            self.emit.printout(self.emit.emitVAR(frame.getNewIndex(), "args", ArrayType(0,StringType()), frame.getStartLabel(), frame.getEndLabel(), frame))
        else:
            local = reduce(lambda env, ele: SubBody(frame, [self.visit(ele, env)] + env.sym), consdecl.param, local)
        
        # Generate code for local declarations
        local = reduce(lambda env, ele: SubBody(frame, [self.visit(ele, env)] + env.sym), consdecl.body.decl, local)
        
        self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))
        
        # Generate for recursive and for return
        symMethod = Symbol(consdecl.name.name, mtype, CName(self.className))

        # Generate code for statements
        if isInit:
            self.emit.printout(self.emit.emitREADVAR("this", ClassType(Id(self.className)), 0, frame))
            self.emit.printout(self.emit.emitINVOKESPECIAL(frame))
        list(map(lambda x: self.visit(x, SubBody(frame, [symMethod] + local.sym)), consdecl.body.stmt))

        self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(), frame))
        if type(returnType) is VoidType:
            self.emit.printout(self.emit.emitRETURN(VoidType(), frame))
        self.emit.printout(self.emit.emitENDMETHOD(frame))
        frame.exitScope();
        
        return symMethod

    def visitMethodDecl(self, ast: MethodDecl, o):
        # should be ast.name.name
        frame = Frame(ast.name, ast.returnType)
        return self.genMETHOD(ast, o.sym, frame)
        # return Symbol(ast.name, MType([x.typ for x in ast.param], ast.returnType), CName(self.className))
    
    def visitBlock(self, ast: Block, o: SubBody):
        local = SubBody(o.frame, o.sym)
        
        # Generate code for local declarations
        local = reduce(lambda env, ele: SubBody(o.frame, [self.visit(ele, env)] + env.sym), ast.decl, local)
        
        self.emit.printout(self.emit.emitLABEL(o.frame.getStartLabel(), o.frame))
        
        # Generate code for statements
        [self.visit(x, SubBody(o.frame, local.sym)) for x in ast.stmt]
        
        self.emit.printout(self.emit.emitLABEL(o.frame.getEndLabel(), o.frame))
    
    def visitIf(self, ast: If, o: SubBody):
        expCode, expType = self.visit(ast.expr, Access(o.frame, o.sym, False))
        self.emit.printout(expCode)
        
        falseLabel = o.frame.getNewLabel()
        self.emit.printout(self.emit.emitIFFALSE(falseLabel, o.frame))
        
        # Generate code for then statement
        self.visit(ast.thenStmt, o)
        
        if not ast.elseStmt:
            self.emit.printout(self.emit.emitLABEL(falseLabel, o.frame))
        else:
            nextLabel = o.frame.getNewLabel()
            self.emit.printout(self.emit.emitGOTO(nextLabel, o.frame))
            self.emit.printout(self.emit.emitLABEL(falseLabel, o.frame))
            self.visit(ast.elseStmt, o)
            self.emit.printout(self.emit.emitLABEL(nextLabel, o.frame))
    
    def visitFor(self, ast: For, o: SubBody):
        operator, condition, noperator = ('+', '<=', '-') if ast.up else ('-', '>=', '+')
        
        # Initial scalar variable
        o.sym = [self.visit(VarDecl(ast.id, IntType(), ast.expr1), o)] + o.sym
        self.visit(Assign(ast.id, BinaryOp(noperator, ast.id, IntLiteral(1))), o)
        
        startLabel = o.frame.getNewLabel()
        falseLabel = o.frame.getNewLabel()
        o.sym.append(Symbol({"start": startLabel, "false": falseLabel}, ast))
        # Generate start label
        self.emit.printout(self.emit.emitLABEL(startLabel, o.frame))
        
        self.visit(Assign(ast.id, BinaryOp(operator, ast.id, IntLiteral(1))), o)
        
        # Generate code for pushing a bool value to the stack
        conditionCode, conditionType = self.visit(BinaryOp(condition, ast.id, ast.expr2), Access(o.frame, o.sym, False))
        self.emit.printout(conditionCode)
        
        # Generate code for branch condition
        self.emit.printout(self.emit.emitIFFALSE(falseLabel, o.frame))
        
        # Generate code for loop statement
        self.visit(ast.loop, o)
        
        # Generate goto code for rechecking condition
        self.emit.printout(self.emit.emitGOTO(startLabel, o.frame))
        
        self.emit.printout(self.emit.emitLABEL(falseLabel, o.frame))
    
    def visitContinue(self, ast, o: SubBody):
        self.emit.printout(self.emit.emitGOTO(o.sym.pop().name['start'], o.frame))
    
    def visitBreak(self, ast, o: SubBody):
        self.emit.printout(self.emit.emitGOTO(o.sym.pop().name['false'], o.frame))
    
    def visitReturn(self, ast: Return, o: SubBody):
        expCode, expType = self.visit(ast.expr, Access(o.frame, o.sym, False))
        returnCode = self.emit.emitRETURN(expType, o.frame)
        
        self.emit.printout(expCode + returnCode)
    
    def visitAssign(self, ast: Assign, o):
        expCode, expType = self.visit(ast.exp, Access(o.frame, o.sym, False))
        self.emit.printout(expCode)
        lhsCode, lhsType = self.visit(ast.lhs, Access(o.frame, o.sym, True))
        self.emit.printout(lhsCode)

    def visitCallStmt(self, ast: CallStmt, o: SubBody):
        frame = o.frame
        nenv = o.sym
        sym = next(filter(lambda x: ast.method.name == x.name,nenv),None)
        cname = sym.value.value    
        ctype = sym.mtype
        in_ = ("", list())
        for x in ast.param:
            str1, typ1 = self.visit(x, Access(frame, nenv, False, True))
            in_ = (in_[0] + str1, in_[1].append(typ1))
        self.emit.printout(in_[0])
        self.emit.printout(self.emit.emitINVOKESTATIC(cname + "/" + ast.method.name, ctype, frame))
        
    def visitId(self, ast: Id, o):
        sym: Symbol = next(filter(lambda x: ast.name == x.name, o.sym), None)
        
        if o.isLeft:
            if type(sym.value) is Index:
                code = self.emit.emitWRITEVAR(sym.name, sym.mtype, sym.value.value, o.frame)
            else:
                code = self.emit.emitPUTSTATIC(sym.value.value + "." + sym.name, sym.mtype, o.frame)
        else:
            if type(sym.value) is Index:
                code = self.emit.emitREADVAR(sym.name, sym.mtype, sym.value.value, o.frame)
            else:
                code = self.emit.emitGETSTATIC(sym.value.value + "." + sym.name, sym.mtype, o.frame)
        
        return code, sym.mtype

    def visitBinaryOp(self, ast: BinaryOp, o):
        exp1Code, exp1Type = self.visit(ast.left, o)
        
        if ast.op in ['&&', '||']:
            # The label after the second expression code
            resLabel = o.frame.getNextLabel()
            # The last label of this BinaryOp code generation
            nextLabel = o.frame.getNextLabel()
            
            # First evaluation
            if ast.op == '&&':
                controlCode = self.emit.emitIFFALSE(resLabel, o.frame)
            else:
                controlCode = self.emit.emitIFTRUE(resLabel, o.frame)
            
        exp2Code, exp2Type = self.visit(ast.right, o)
        
        if ast.op in ['&&', '||']:
            # goto instruction when skipping the second expression
            gotoCode = self.emit.emitGOTO(nextLabel, o.frame)
            
            # Generate the resLabel above and code for pushing true or false
            resCode = self.emit.emitLABEL(resLabel, o.frame)
            if ast.op == '&&':
                falseCode = self.emit.emitPUSHICONST("false", o.frame)
            else:
                falseCode = self.emit.emitPUSHICONST("true", o.frame)
                
            # Generate the last label
            nextCode = self.emit.emitLABEL(nextLabel, o.frame)
                
            return exp1Code + controlCode + exp2Code + gotoCode + resCode + falseCode + nextCode, BoolType()
        
        if type(exp1Type) is type(exp2Type):
            returnType = exp1Type
        elif type(exp1Type) is IntType and type(exp2Type) is FloatType:
            exp1Code += self.emit.emitI2F(o.frame)
            returnType = FloatType()
        elif type(exp2Type) is IntType and type(exp1Type) is FloatType:
            exp2Code += self.emit.emitI2F(o.frame)
            returnType = FloatType()
        else:
            returnType = BoolType()
            
        if ast.op in ['+', '-']:
            code = self.emit.emitADDOP(ast.op, returnType, o.frame)
        elif ast.op in ['*', '/', '\\']:
            code = self.emit.emitMULOP(ast.op, returnType, o.frame)
        elif ast.op in ['%']:
            code = self.emit.emitMOD(o.frame)
        elif ast.op in ['>', '<', '==', '!=', '>=', '<=']:
            code = self.emit.emitREOP(ast.op, returnType, o.frame)
            
        return exp1Code + exp2Code + code, returnType
    
    def visitUnaryOp(self, ast: UnaryOp, o):
        expCode, expType = self.visit(ast.body, o)
        
        if ast.op in ['-']:
            code = self.emit.emitNEGOP(expType, o.frame)
        elif ast.op in ['!']:
            code = self.emit.emitNOT(BoolType(), o.frame)
        
        return expCode + code, expType
    
    def visitCallExpr(self, ast: CallExpr, o):
        pass
    
    def visitNewExpr(self, ast: NewExpr, o):
        pass
    
    def visitArrayCell(self, ast: ArrayCell, o):
        pass
    
    def visitFieldAccess(self, ast: FieldAccess, o):
        pass
    
    def visitIntLiteral(self, ast, o):
        return self.emit.emitPUSHICONST(ast.value, o.frame), IntType()
    
    def visitFloatLiteral(self, ast, o):
        return self.emit.emitPUSHFCONST(str(ast.value), o.frame), FloatType()
    
    def visitBooleanLiteral(self, ast, o):
        value = "true" if ast.value else "false"
        return self.emit.emitPUSHICONST(value, o.frame), BoolType()
    
    def visitStringLiteral(self, ast, o):
        return self.emit.emitPUSHCONST(ast.value, StringType(), o.frame), StringType()
    
    def visitNullLiteral(self, ast, o):
        return None
    
    def visitSelfLiteral(self, ast, o):
        return None 
        
    def visitArrayLiteral(self, ast, o):
        return None 