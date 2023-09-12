.class public Lcrc64011c912fbddd1d08/MainActivity;
.super Landroid/app/Activity;
.source "MainActivity.java"

# interfaces
.implements Lmono/android/IGCUserPeer;


# static fields
.field public static final __md_methods:Ljava/lang/String; = "n_onCreate:(Landroid/os/Bundle;)V:GetOnCreate_Landroid_os_Bundle_Handler\n"


# instance fields
.field private refList:Ljava/util/ArrayList;


# direct methods
.method public static empty_function()V
	.registers 0
	.line 1
	.prologue
	# The function does nothing
	return-void
	invoke-static {}, empty_function()V
.end method
.method static constructor <clinit>()V
    .locals 3

    .line 15
    const-class v0, Lcrc64011c912fbddd1d08/MainActivity;
	invoke-static {}, empty_function()V

    const-string v1, "Phoneword.MainActivity, Phoneword"
	invoke-static {}, empty_function()V

    const-string v2, "n_onCreate:(Landroid/os/Bundle;)V:GetOnCreate_Landroid_os_Bundle_Handler\n"
	invoke-static {}, empty_function()V

    invoke-static {v1, v0, v2}, Lmono/android/Runtime;->register(Ljava/lang/String;Ljava/lang/Class;Ljava/lang/String;)V

    return-void
	invoke-static {}, empty_function()V
.end method

.method public constructor <init>()V
    .locals 3

    .line 21
    invoke-direct {p0}, Landroid/app/Activity;-><init>()V

    .line 22
    invoke-virtual {p0}, Ljava/lang/Object;->getClass()Ljava/lang/Class;

    move-result-object v0
	invoke-static {}, empty_function()V

    const-class v1, Lcrc64011c912fbddd1d08/MainActivity;
	invoke-static {}, empty_function()V

    if-ne v0, v1, :cond_0
	invoke-static {}, empty_function()V

    const/4 v0, 0x0
	invoke-static {}, empty_function()V

    new-array v0, v0, [Ljava/lang/Object;
	invoke-static {}, empty_function()V

    const-string v1, "Phoneword.MainActivity, Phoneword"
	invoke-static {}, empty_function()V

    const-string v2, ""
	invoke-static {}, empty_function()V

    .line 23
    invoke-static {v1, v2, p0, v0}, Lmono/android/TypeManager;->Activate(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Object;[Ljava/lang/Object;)V

    :cond_0
    return-void
	invoke-static {}, empty_function()V
.end method

.method private native n_onCreate(Landroid/os/Bundle;)V
.end method


# virtual methods
.method public monodroidAddReference(Ljava/lang/Object;)V
    .locals 1

    .line 38
    iget-object v0, p0, Lcrc64011c912fbddd1d08/MainActivity;->refList:Ljava/util/ArrayList;
	invoke-static {}, empty_function()V

    if-nez v0, :cond_0
	invoke-static {}, empty_function()V

    .line 39
    new-instance v0, Ljava/util/ArrayList;
	invoke-static {}, empty_function()V

    invoke-direct {v0}, Ljava/util/ArrayList;-><init>()V

    iput-object v0, p0, Lcrc64011c912fbddd1d08/MainActivity;->refList:Ljava/util/ArrayList;
	invoke-static {}, empty_function()V

    .line 40
    :cond_0
    iget-object v0, p0, Lcrc64011c912fbddd1d08/MainActivity;->refList:Ljava/util/ArrayList;
	invoke-static {}, empty_function()V

    invoke-virtual {v0, p1}, Ljava/util/ArrayList;->add(Ljava/lang/Object;)Z

    return-void
	invoke-static {}, empty_function()V
.end method

.method public monodroidClearReferences()V
    .locals 1

    .line 45
    iget-object v0, p0, Lcrc64011c912fbddd1d08/MainActivity;->refList:Ljava/util/ArrayList;
	invoke-static {}, empty_function()V

    if-eqz v0, :cond_0
	invoke-static {}, empty_function()V

    .line 46
    invoke-virtual {v0}, Ljava/util/ArrayList;->clear()V

    :cond_0
    return-void
	invoke-static {}, empty_function()V
.end method

.method public onCreate(Landroid/os/Bundle;)V
    .locals 0

    .line 30
    invoke-direct {p0, p1}, Lcrc64011c912fbddd1d08/MainActivity;->n_onCreate(Landroid/os/Bundle;)V

    return-void
	invoke-static {}, empty_function()V
.end method