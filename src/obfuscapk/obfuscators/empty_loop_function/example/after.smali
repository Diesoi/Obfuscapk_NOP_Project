.class public final Lphoneword/phoneword/R;
.super Ljava/lang/Object;
.source "R.java"


# annotations
.annotation system Ldalvik/annotation/MemberClasses;
    value = {
        Lphoneword/phoneword/R$string;,
        Lphoneword/phoneword/R$layout;,
        Lphoneword/phoneword/R$id;,
        Lphoneword/phoneword/R$drawable;
    }
.end annotation


.class public Lcom/obfuscapk/demo/NopDemo;
.super Ljava/lang/Object;
.source "NopDemo.java"


# direct methods
.method public static empty_loop_function()V
	.registers 4
	const/4 v0, 0
	:loop_start
	add-int/lit8 v0, v0, 1
	const/16 v1, 1
	if-lt v0, v1, :loop_start
	return-void
.end method
.method public constructor <init>()V
    .locals 0

    .line 3
	invoke-static {}, empty_loop_function()V
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static getNopMessage(Ljava/lang/String;)Ljava/lang/String;
    .locals 2

    .line 8
    new-instance v0, Ljava/lang/StringBuilder;

	invoke-static {}, empty_loop_function()V
    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    const-string v1, "Nop message: "

	invoke-static {}, empty_loop_function()V
    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v1, "sending a nop message from "

	invoke-static {}, empty_loop_function()V
    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

	invoke-static {}, empty_loop_function()V
    invoke-virtual {v0, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

	invoke-static {}, empty_loop_function()V
    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    return-object p0
.end method