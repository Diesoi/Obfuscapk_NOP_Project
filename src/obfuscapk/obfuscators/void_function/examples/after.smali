.class public Lcom/obfuscapk/demo/NopDemo;
.super Ljava/lang/Object;
.source "NopDemo.java"


# direct methods
.method public static BRaLxVs6y()V
	.registers 2
	const/4 v0, 0x4
	const/4 v1, 0x1
	add-int v0, v0, v1
	return-void
.end method
.method public constructor <init>()V
    .locals 0

    .line 3
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    return-void
.end method

.method public static getNopMessage(Ljava/lang/String;)Ljava/lang/String;
    .locals 2

    .line 8
    new-instance v0, Ljava/lang/StringBuilder;

	invoke-static {}, BRaLxVs6y()V
    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    const-string v1, "Nop message: "

	invoke-static {}, BRaLxVs6y()V
    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v1, "sending a nop message from "

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    return-object p0
.end method