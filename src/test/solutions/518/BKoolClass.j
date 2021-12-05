.source BKoolClass.java
.class public BKoolClass
.super java.lang.Object

.method public static main([Ljava/lang/String;)V
.var 0 is args [Ljava/lang/String; from Label0 to Label1
.var 1 is a I from Label0 to Label1
	bipush 10
	bipush 7
	iadd
	istore_1
.var 2 is b I from Label0 to Label1
	iload_1
	iconst_3
	irem
	istore_2
Label0:
	iload_1
	iconst_2
	irem
	iload_2
	iconst_1
	isub
	if_icmpne Label2
	iconst_1
	goto Label3
Label2:
	iconst_0
Label3:
	ifle Label4
.var 3 is c I from Label0 to Label1
	bipush 12
	iload_2
	isub
	istore_3
Label0:
	iload_3
	invokestatic io/writeInt(I)V
Label1:
Label4:
Label1:
	return
.limit stack 4
.limit locals 4
.end method

.method public <init>()V
.var 0 is this LBKoolClass; from Label0 to Label1
Label0:
	aload_0
	invokespecial java/lang/Object/<init>()V
Label1:
	return
.limit stack 1
.limit locals 1
.end method
