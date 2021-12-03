import unittest
from TestUtils import TestCodeGen
from AST import *


class CheckCodeGenSuite(unittest.TestCase):
    # def test_bkool_int_ast(self):
    #     input = """class BKoolClass {static void main() {io.writeInt(1);}}"""
    #     expect = "1"
    #     self.assertTrue(TestCodeGen.test(input,expect,500))
    # def test_bkool_bin_ast(self):
    #     input = """class BKoolClass {static void main() {io.writeInt(1+3);}}"""
    #     expect = "4"
    #     self.assertTrue(TestCodeGen.test(input,expect,501))
    # def test_int_ast(self):
    # 	input = Program([ClassDecl(Id("BKoolClass"),
    #                         [MethodDecl(Static(),Id("main"),[],VoidType(),
    #                             Block([],[CallStmt(Id("io"),Id("writeInt"),[IntLiteral(1)])]))])])
    # 	expect = "1"
    # 	self.assertTrue(TestCodeGen.test(input,expect,502))
    # def test_binary_ast(self):
    #     input = Program([ClassDecl(Id("BKoolClass"),
    #                 [MethodDecl(Static(),Id("main"),[],VoidType(),
    #                     Block([],[CallStmt(Id("io"),Id("writeInt"),[BinaryOp("+",IntLiteral(1),IntLiteral(3))])]))])])
    #     expect = "4"
    #     self.assertTrue(TestCodeGen.test(input,expect,503))
        
    # def test_bkool_float_ast(self):
    #     input = """class BKoolClass {
    #             static void main() {
    #                 io.writeFloat(1.2 + 1);
    #             }
    #         }"""
    #     expect = "2.2"
    #     self.assertTrue(TestCodeGen.test(input,expect,504))
        
    # def test_bkool_div_ast(self):
    #     input = """class BKoolClass {
    #             static void main() {
    #                 io.writeInt(2 \ 1);
    #             }
    #         }"""
    #     expect = "2"
    #     self.assertTrue(TestCodeGen.test(input,expect,505))
        
    # def test_bkool_vardecl_ast(self):
    #     input = """class BKoolClass {
    #             static void main() {
    #                 int a;
    #                 a := 12;
    #                 io.writeInt(a);
    #             }
    #         }"""
    #     expect = "12"
    #     self.assertTrue(TestCodeGen.test(input,expect,506))
        
    # def test_bkool_vardecl1(self):
    #     input = """class BKoolClass {
    #             static void main() {
    #                 float a;
    #                 a := 12.2;
    #                 io.writeFloat(a);
    #             }
    #         }"""
    #     expect = "12.2"
    #     self.assertTrue(TestCodeGen.test(input,expect,507))
    
    # def test_bkool_vardecl2(self):
    #     input = """class BKoolClass {
    #             static void main() {
    #                 string a;
    #                 a := "ngoductri";
    #                 io.writeStr(a);
    #             }
    #         }"""
    #     expect = "ngoductri"
    #     self.assertTrue(TestCodeGen.test(input,expect,508))
    
    # def test_bkool_unary_op(self):
    #     input = """class BKoolClass {
    #             static void main() {
    #                 int a, b;
    #                 a := 5;
    #                 b := -a;
    #                 io.writeInt(b);
    #             }
    #         }"""
    #     expect = "-5"
    #     self.assertTrue(TestCodeGen.test(input,expect,509))
        
    # def test_bkool_mod(self):
    #     input = """class BKoolClass {
    #             static void main() {
    #                 int a, b;
    #                 a := 17;
    #                 b := a % 3;
    #                 io.writeInt(b);
    #             }
    #         }"""
    #     expect = "2"
    #     self.assertTrue(TestCodeGen.test(input,expect,510))
        
    def test_bkool_initial(self):
        input = """class BKoolClass {
                static void main() {
                    int a = 10 + 7;
                    int b = a % 3;
                    io.writeInt(b);
                }
            }"""
        expect = "2"
        self.assertTrue(TestCodeGen.test(input,expect,511))