# ------------------------------------------------------------------------------
# Equivalent OpenSees TCL Script for a 3D Beam Modal Analysis
# ------------------------------------------------------------------------------

#
# 1. Basic Model Settings
#
model BasicBuilder -ndm 3 -ndf 6

# Number of segments & geometry (similar to the Python script)
# The Python script has n=50 'stations', so 49 line elements
set n 50
# Length of each segment in meters
set l 0.1

# ------------------------------------------------------------------------------
# 2. Define Nodes
#    We create 50 nodes (index 1..50), spaced by 'l' along the X-axis.
# ------------------------------------------------------------------------------
for {set i 0} {$i < $n} {incr i} {
    set x [expr $i*$l]
    # node <tag> <x> <y> <z>
    node [expr $i+1] $x 0.0 0.0
}

# ------------------------------------------------------------------------------
# 3. Material & Section Properties (Elastic Beam)
#    Based on the Python example:
#      E     = 210 GPa,  v = 0.2, density = 7800 kg/m^3
#      ISection with w=100 mm, h=190 mm, tw=2 mm, tf=2 mm (approx. calculations).
# ------------------------------------------------------------------------------
set E 2.1e11        ;# Young's modulus [N/m^2]
set nu 0.20         ;# Poisson's ratio
set rho 7800.0      ;# density [kg/m^3]

# Shear modulus G = E/(2*(1+nu))
set G [expr $E/(2.0*(1.0+$nu))]

# Approx. cross section (convert mm to m if needed):
# A  ~ 7.72e-4 m^2
# Iy ~ 3.33e-7 m^4  (minor axis)
# Iz ~ 4.61e-6 m^4  (major axis)
# J  ~ 1.03e-9 m^4  (torsion constant, approximate)
set A  7.72e-4
set Iy 3.33e-7
set Iz 4.61e-6
set J  1.03e-9

# Create an elastic section
# NOTE: The order of arguments for 'section Elastic' in 3D is:
#       section Elastic <secTag> E A Iz Iy G J
section Elastic 1 $E $A $Iz $Iy $G $J

# ------------------------------------------------------------------------------
# 4. Define Geometric Transformation
#    This aligns the local y-axis with global Y, for instance.
# ------------------------------------------------------------------------------
geomTransf Linear 1 0 1 0

# ------------------------------------------------------------------------------
# 5. Define Elements (elasticBeamColumn)
#    We have 49 beam elements, each connecting node i to node i+1.
# ------------------------------------------------------------------------------
set elemID 1
for {set i 1} {$i < $n} {incr i} {
    set j [expr $i+1]
    # element elasticBeamColumn <eleTag> <iNode> <jNode> <secTag> <transfTag>
    element elasticBeamColumn $elemID $i $j 1 1
    incr elemID
}

# ------------------------------------------------------------------------------
# 6. Boundary Conditions
#    Fix the first node (x=0) in all 6 DOFs,
#    just like the Python script's 'add_fix_bc()' at the start.
# ------------------------------------------------------------------------------
fix 1 1 1 1 1 1 1

# ------------------------------------------------------------------------------
# 7. Assign Mass
#    For a modal analysis, we must define mass. We'll do a simple uniform
#    'lumped-mass' approach: each node gets (total_mass / n).
# ------------------------------------------------------------------------------
# Total length = (n-1)*l
set totalLength [expr ($n-1)*$l]

# Cross-sectional area * total length = total volume
set totalVolume [expr $A*$totalLength]

# totalMass = density * totalVolume
set totalMass [expr $rho*$totalVolume]

# lumped mass at each node = totalMass / n
set nodeMass [expr $totalMass/$n]

# Because it's a 3D model with 6 DOF, we set mass for the 3 translational DOFs.
# Rotational mass (moments of inertia) are omitted for simplicity.
for {set i 1} {$i <= $n} {incr i} {
    mass $i $nodeMass $nodeMass $nodeMass 0.0 0.0 0.0
}

# ------------------------------------------------------------------------------
# 8. Modal Analysis
#    We'll request 6 eigenmodes (like in the Python script).
# ------------------------------------------------------------------------------
set numModes 6

# Define a simple system/analysis setup for the eigenvalue solver
system BandGeneral
constraints Plain
numberer RCM
test NormUnbalance 1.0e-12 100
algorithm Linear
integrator Newmark 0.5 0.25
analysis Transient

# Compute eigenvalues (lambda) for the first 'numModes' modes
set eigenValues [eigen $numModes]

puts "------------------------------------------------------------"
puts "Modal Analysis Results:"
puts "  Mode :   Lambda        Omega (rad/s)    Freq (Hz)"
puts "------------------------------------------------------------"

for {set iMode 1} {$iMode <= $numModes} {incr iMode} {
    # lambda = eigenvalue
    set lambda   [lindex $eigenValues [expr $iMode-1]]
    set omega    [expr sqrt($lambda)]            ;# rad/s
    set freqHz   [expr $omega/(2.0*3.14159265359)]
    puts "   $iMode   :   $lambda   $omega   $freqHz"
}

puts "------------------------------------------------------------"
puts "Done."