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
    #     input = Program([ClassDecl(Id("BKoolClass"),[MethodDecl(Static(),Id("main"),[],VoidType(),Block([],[CallStmt(Id("io"),Id("writeInt"),[IntLiteral(1)])]))])])
    #     expect = "1"
    #     self.assertTrue(TestCodeGen.test(input,expect,502))
     
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
        
    # def test_bkool_initial(self):
    #     input = """class BKoolClass {
    #             static void main() {
    #                 int a = 10 + 7;
    #                 int b = a % 3;
    #                 io.writeInt(b);
    #             }
    #         }"""
    #     expect = "2"
    #     self.assertTrue(TestCodeGen.test(input,expect,511))
        
    # def test_bkool_ifstmt1(self):
    #     input = """class BKoolClass {
    #             static void main() {
    #                 int a = 10 + 7;
    #                 int b = a % 3;
    #                 if a % 2 == 1 then io.writeInt(b);
    #             }
    #         }"""
    #     expect = "2"
    #     self.assertTrue(TestCodeGen.test(input,expect,512))
        
    # def test_bkool_ifstmt2(self):
    #     input = """class BKoolClass {
    #             static void main() {
    #                 int a = 10 + 7;
    #                 int b = a % 3;
    #                 if a % 2 != 1 then
    #                     io.writeInt(b);
    #                 else
    #                     io.writeInt(a);
    #             }
    #         }"""
    #     expect = "17"
    #     self.assertTrue(TestCodeGen.test(input,expect,513))
        
    # def test_bkool_ifstmt3(self):
    #     input = """class BKoolClass {
    #             static void main() {
    #                 int a = 10 + 7;
    #                 int b = a % 3;
    #                 if a % 2 != b - 1 then
    #                     io.writeInt(b);
    #                 else
    #                     io.writeInt(a);
    #             }
    #         }"""
    #     expect = "17"
    #     self.assertTrue(TestCodeGen.test(input,expect,514))
        
    # def test_bkool_block1(self):
    #     input = """class BKoolClass {
    #             static void main() {
    #                 int a = 10 + 7;
    #                 int b = a % 3;
    #                 if a % 2 == b - 2 then {
    #                     io.writeInt(b);
    #                 }
    #                 else {
    #                     int c = 5;
    #                     io.writeInt(c);
    #                 }
    #             }
    #         }"""
    #     expect = "5"
    #     self.assertTrue(TestCodeGen.test(input,expect,515))
        
    # def test_bkool_block2(self):
    #     input = """class BKoolClass {
    #             static void main() {
    #                 int a = 10 + 7;
    #                 int b = a % 3;
    #                 if a % 2 == b - 2 then {
    #                     io.writeInt(b);
    #                 }
    #                 else {
    #                     int c = 5;
    #                     io.writeInt(c);
    #                 }
    #                 io.writeInt(a);
    #             }
    #         }"""
    #     expect = "517"
    #     self.assertTrue(TestCodeGen.test(input,expect,516))
        
    # def test_bkool_constant1(self):
    #     input = """class BKoolClass {
    #             static void main() {
    #                 final int a = 10 + 7;
    #                 int b = a % 3;
    #                 if a % 2 == b - 1 then {
    #                     final float c = 12.3;
    #                     io.writeFloat(c);
    #                 }
    #             }
    #         }"""
    #     expect = "12.3"
    #     self.assertTrue(TestCodeGen.test(input,expect,517))
        
    # def test_bkool_constant2(self):
    #     input = """class BKoolClass {
    #             static void main() {
    #                 final int a = 10 + 7;
    #                 int b = a % 3;
    #                 if a % 2 == b - 1 then {
    #                     final int c = 12 - b;
    #                     io.writeInt(c);
    #                 }
    #             }
    #         }"""
    #     expect = "10"
    #     self.assertTrue(TestCodeGen.test(input,expect,518))
        
    def test_bkool_constant3(self):
        input = """class BKoolClass {
                static void main() {
                    final int a = 10 + 7;
                    int b = a % 3;
                    if a % 2 == b - 1 then {
                        final int c = 12 - a;
                        io.writeInt(c);
                    }
                }
            }"""
        expect = "-5"
        self.assertTrue(TestCodeGen.test(input,expect,519))