.source BKoolClass.java
.class public BKoolClass
.super java.lang.Object

.method public static main([Ljava/lang/String;)V
.var 0 is args [Ljava/lang/String; from Label0 to Label1
.var 1 is b I from Label0 to Label1
	iconst_5
	istore_1
Label0:
.var 2 is x I from Label0 to Label1
	iconst_2
	ineg
	istore_2
	iload_2
	iconst_1
	iadd
	istore_2
Label2:
	iload_2
	iconst_1
	isub
	istore_2
	iload_2
	iconst_5
	ineg
	if_icmplt Label4
	iconst_1
	goto Label5
Label4:
	iconst_0
Label5:
	ifle Label3
	iload_1
	invokestatic io/writeInt(I)V
	goto Label2
Label3:
Label1:
	return
.limit stack 3
.limit locals 3
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
