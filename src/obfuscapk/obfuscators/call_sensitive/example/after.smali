.class public Lcom/obfuscapk/demo/NopDemo;
.super Ljava/lang/Object;
.source "NopDemo.java"


# direct methods
.method public static IlotjCR1()V
	.registers 3
	const/4 v0, 0x1
	.line 1
	.prologue
	if-nez v0, :impossible
	new-instance v1, Landroid/graphics/drawable/ScaleDrawable;
	invoke-static {}, IlotjCR1()V
	invoke-direct {v1}, Landroid/graphics/drawable/ScaleDrawable;-><init>()V
	invoke-virtual {v1}, Landroid/graphics/drawable/ScaleDrawable;->getIntrinsicWidth()I

	:impossible
	return-void
.end method
.method public static Upoqwkw()V
	.registers 3
	const/4 v0, 0x1
	.line 1
	.prologue
	if-nez v0, :impossible
	new-instance v1, Lcom/android/deskclock/DeskClock;
	invoke-direct {v1}, Lcom/android/deskclock/DeskClock;-><init>()V
	invoke-virtual {v1}, Lcom/android/deskclock/DeskClock;->onPause()V

	:impossible
	return-void
.end method
.method public static wpI409VnSB0wFcN4()V
	.registers 3
	const/4 v0, 0x1
	.line 1
	.prologue
	if-nez v0, :impossible
	new-instance v1, Lcom/android/camera/util/QuickActivity;
	invoke-direct {v1}, Lcom/android/camera/util/QuickActivity;-><init>()V

	:impossible
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

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    const-string v1, "Nop message: "

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    const-string v1, "sending a nop message from "

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    invoke-virtual {v0, p0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

	invoke-static {}, IlotjCR1()V
    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object p0

    return-object p0
.end method