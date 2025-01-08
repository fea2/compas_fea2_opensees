# zeroLengthContactNTS2D_Example2.tcl 

######################## 
# Analysis-Sequence  1 #
######################## 

wipe

# Start of model generation 
# ========================= 

# Create ModelBuilder 
# ------------------- 
model  BasicBuilder  -ndm  2  -ndf  2 

# Define geometry 
# ---------------
# NodeCoord.tcl 

# Node    tag    xCrd    yCrd 
node   1  0  0 
node   2  1  0 
node   3  2  0 
node   4  3  0 
node   5  4  0 
node   6  5  0 
node   7  6  0 
node   8  7  0 
node   9  8  0 
node  10  9  0 
node  11  10  0 
node  12  0  1 
node  13  1  1 
node  14  2  1 
node  15  3  1 
node  16  4  1 
node  17  5  1 
node  18  6  1 
node  19  7  1 
node  20  8  1 
node  21  9  1 
node  22  10  1 
node  23  0  1 
node  24  1  1 
node  25  2  1 
node  26  3  1 
node  27  4  1 
node  28  5  1 
node  29  6  1 
node  30  7  1 
node  31  8  1 
node  32  9  1 
node  33  10  1 
node  34  0  2 
node  35  1  2 
node  36  2  2 
node  37  3  2 
node  38  4  2 
node  39  5  2 
node  40  6  2 
node  41  7  2 
node  42  8  2 
node  43  9  2 
node  44  10  2


# Define Single Point Constraints 
# ------------------------------- 
# SPConstraint.tcl 

# SPC    tag    Dx    Dy 
fix       1     1     1 
fix      12     1     1 
fix      23     1     1 
fix      34     1     1 

# Define material(s) 
# ------------------ 
# Materials.tcl 

# Material "Material01":    matTag    E    v    rho 
nDMaterial ElasticIsotropic   1   1e5   0.25  6.75 

# Define element(s) 
# ----------------- 
# Elements.tcl 

# Element "Element01":    eleTag    NodeI    NodeJ    NodeK    NodeL    h    type    matTag     
element  quad       1       1       2      13      12  1  "PlaneStrain"       1   
# Element "Element01":    eleTag    NodeI    NodeJ    NodeK    NodeL    h    type    matTag     
element  quad       2       2       3      14      13  1  "PlaneStrain"       1   
# Element "Element01":    eleTag    NodeI    NodeJ    NodeK    NodeL    h    type    matTag     
element  quad       3       3       4      15      14  1  "PlaneStrain"       1   
# Element "Element01":    eleTag    NodeI    NodeJ    NodeK    NodeL    h    type    matTag     
element  quad       4       4       5      16      15  1  "PlaneStrain"       1   
# Element "Element01":    eleTag    NodeI    NodeJ    NodeK    NodeL    h    type    matTag     
element  quad       5       5       6      17      16  1  "PlaneStrain"       1   
# Element "Element01":    eleTag    NodeI    NodeJ    NodeK    NodeL    h    type    matTag     
element  quad       6       6       7      18      17  1  "PlaneStrain"       1   
# Element "Element01":    eleTag    NodeI    NodeJ    NodeK    NodeL    h    type    matTag     
element  quad       7       7       8      19      18  1  "PlaneStrain"       1   
# Element "Element01":    eleTag    NodeI    NodeJ    NodeK    NodeL    h    type    matTag     
element  quad       8       8       9      20      19  1  "PlaneStrain"       1   
# Element "Element01":    eleTag    NodeI    NodeJ    NodeK    NodeL    h    type    matTag     
element  quad       9       9      10      21      20  1  "PlaneStrain"       1   
# Element "Element01":    eleTag    NodeI    NodeJ    NodeK    NodeL    h    type    matTag     
element  quad      10      10      11      22      21  1  "PlaneStrain"       1   
# Element "Element01":    eleTag    NodeI    NodeJ    NodeK    NodeL    h    type    matTag     
element  quad      11      23      24      35      34  1  "PlaneStrain"       1   
# Element "Element01":    eleTag    NodeI    NodeJ    NodeK    NodeL    h    type    matTag     
element  quad      12      24      25      36      35  1  "PlaneStrain"      1   
# Element "Element01":    eleTag    NodeI    NodeJ    NodeK    NodeL    h    type    matTag     
element  quad      13      25       26      37      36  1  "PlaneStrain"       1   
# Element "Element01":    eleTag    NodeI    NodeJ    NodeK    NodeL    h    type    matTag     
element  quad      14      26       27      38      37  1  "PlaneStrain"       1   
# Element "Element01":    eleTag    NodeI    NodeJ    NodeK    NodeL    h    type    matTag     
element  quad      15      27       28      39      38  1  "PlaneStrain"       1   
# Element "Element01":    eleTag    NodeI    NodeJ    NodeK    NodeL    h    type    matTag     
element  quad      16      28       29      40      39  1  "PlaneStrain"       1   
# Element "Element01":    eleTag    NodeI    NodeJ    NodeK    NodeL    h    type    matTag     
element  quad      17      29       30      41      40  1  "PlaneStrain"       1   
# Element "Element01":    eleTag    NodeI    NodeJ    NodeK    NodeL    h    type    matTag     
element  quad      18      30       31      42      41  1  "PlaneStrain"       1   
# Element "Element01":    eleTag    NodeI    NodeJ    NodeK    NodeL    h    type    matTag     
element  quad      19      31      32      43      42  1  "PlaneStrain"       1   
# Element "Element01":    eleTag    NodeI    NodeJ    NodeK    NodeL    h    type    matTag     
element  quad      20      32      33      44      43  1  "PlaneStrain"       1   
# ZeroLengthContactNTS2Dnd  $eleID $sNdNum $mNdNum $Nodes $Kn $Kt $fs 
element zeroLengthContactNTS2D 21 -sNdNum 11 -mNdNum 11 -Nodes 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 1e10 1e10 0

# Start of anaysis generation 
# =========================== 

# Analysis: StaticDefaultCase 
# +++++++++++++++++++++++++++ 

# Define load pattern 
# ------------------- 
# LoadPattern.tcl 

# LoadPattern "PlainDefault":    patternTag    TimeSeries 
pattern  Plain   1  Constant  { 
    # Load    nodeTag    LoadValues 
    load      44  0  -1.0e02
     # SP    nodeTag    dofTag    DispValue 
     # eleLoad    eleTags    beamUniform    Wy    <Wx> 
     # eleLoad    eleTags    beamPoint    Py    xL    <Px> 
} 

# Define recorder(s) 
# -------------------- 
# Recorder.tcl 

# Node Recorder "DefoShape":    fileName    <nodeTag>    dof    respType 
recorder  Node  -file  Node_Dsp.out  -node 44 -dof  1  2  disp 

# Define analysis options 
# ----------------------- 

# Analysis.tcl 

# AnalysisOptn "StaticDefault": Type: Static 
# ------------------------------------------ 

integrator DisplacementControl 44 2 -1.0e-03
# Convergence test
#                tolerance maxIter displayCode
test EnergyIncr  1.0e-6    100         5
#test NormUnbalance 1e-2 100
# Solution algorithm
algorithm Newton
# DOF numberer
numberer RCM
# Cosntraint handler
#constraints Plain
constraints Transformation
# System of equations solver
system ProfileSPD
# Analysis for gravity load
analysis Static


analyze     500

# Display
# ----------------------- 
# Display.tcl 

# create the display
recorder display g3 10 10 800 800 -wipe
prp 20 5.0 100.0
vup 0 1 0
viewWindow -10 10 -10 10
display 1 4 5

 

