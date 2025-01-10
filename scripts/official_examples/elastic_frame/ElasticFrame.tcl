# OpenSees -- Open System for Earthquake Engineering Simulation
# Pacific Earthquake Engineering Research Center
# http://opensees.berkeley.edu/
#
# Basic Elastic Frame
# ----------------------
#  2d Elastic Beam Column Elements
#  Distributed Load & Pushover Analysis
# 
# Example Objectives
# -----------------
#  Simple Introduction to OpenSees
# 
# Units: kips, in, sec
# Written: fmk
# Date: January 2011

#
# set some parameter
#
set PI  [expr 2.0 * asin(1.0)]
set g   386.4
set ft  12.0
set Load1 1185.0; 
set Load2 1185.0; 
set Load3  970.0;

# set floor masses
set m1  [expr $Load1/(4*$g)]; # 4 nodes per floor
set m2  [expr $Load2/(4*$g)]
set m3  [expr $Load3/(4*$g)]

# set floor distributed loads
set w1  [expr $Load1/(90*$ft)];   # frame 90 ft long
set w2  [expr $Load2/(90*$ft)]
set w3  [expr $Load3/(90*$ft)]

# ------------------------------
# Start of model generation
# ------------------------------

# Remove existing model
wipe

# Create ModelBuilder (with two-dimensions and 2 DOF/node)
model BasicBuilder -ndm 2 -ndf 3

# Create nodes
# ------------

# Create nodes & add to Domain - command: node nodeId xCrd yCrd <-mass $massX $massY $massRz>
# NOTE: mass in optional
node 1     0.0   0.0 
node 2   360.0   0.0 
node 3   720.0   0.0 
node 4  1080.0   0.0 
node 5    0.0  162.0 -mass $m1 $m1 0.0
node 6  360.0  162.0 -mass $m1 $m1 0.0
node 7  720.0  162.0 -mass $m1 $m1 0.0
node 8 1080.0  162.0 -mass $m1 $m1 0.0
node 9     0.0 324.0 -mass $m2 $m2 0.0
node 10  360.0 324.0 -mass $m2 $m2 0.0
node 11  720.0 324.0 -mass $m2 $m2 0.0
node 12 1080.0 324.0 -mass $m2 $m2 0.0
node 13    0.0 486.0 -mass $m3 $m3 0.0
node 14  360.0 486.0 -mass $m3 $m3 0.0
node 15  720.0 486.0 -mass $m3 $m3 0.0
node 16 1080.0 486.0 -mass $m3 $m3 0.0

# Set the boundary conditions - command: fix nodeID xResrnt? yRestrnt? rZRestrnt?
fix 1 1 1 1
fix 2 1 1 1
fix 3 1 1 1
fix 4 1 1 1

# Define geometric transformations for beam-column elements
geomTransf Linear 1; # beams
geomTransf PDelta 2; # columns

# Define elements
# Create elastic beam-column - command: element elasticBeamColumn eleID node1 node2 A E Iz geomTransfTag

# Define the Columns
element elasticBeamColumn  1  1  5 75.6 29000.0 3400.0 2; # W14X257
element elasticBeamColumn  2  5  9 75.6 29000.0 3400.0 2; # W14X257
element elasticBeamColumn  3  9 13 75.6 29000.0 3400.0 2; # W14X257
element elasticBeamColumn  4  2  6 91.4 29000.0 4330.0 2; # W14X311
element elasticBeamColumn  5  6 10 91.4 29000.0 4330.0 2; # W14X311
element elasticBeamColumn  6 10 14 91.4 29000.0 4330.0 2; # W14X311
element elasticBeamColumn  7  3  7 91.4 29000.0 4330.0 2; # W14X311
element elasticBeamColumn  8  7 11 91.4 29000.0 4330.0 2; # W14X311
element elasticBeamColumn  9 11 15 91.4 29000.0 4330.0 2; # W14X311
element elasticBeamColumn 10  4  8 75.6 29000.0 3400.0 2; # W14X257
element elasticBeamColumn 11  8 12 75.6 29000.0 3400.0 2; # W14X257
element elasticBeamColumn 12 12 16 75.6 29000.0 3400.0 2; # W14X257

# Define the Beams
element elasticBeamColumn 13  5  6 34.7 29000.0 5900.0 1; # W33X118
element elasticBeamColumn 14  6  7 34.7 29000.0 5900.0 1; # W33X118
element elasticBeamColumn 15  7  8 34.7 29000.0 5900.0 1; # W33X118
element elasticBeamColumn 16  9 10 34.2 29000.0 4930.0 1; # W30X116
element elasticBeamColumn 17 10 11 34.2 29000.0 4930.0 1; # W30X116
element elasticBeamColumn 18 11 12 34.2 29000.0 4930.0 1; # W30X116
element elasticBeamColumn 19 13 14 20.1 29000.0 1830.0 1; # W24X68
element elasticBeamColumn 20 14 15 20.1 29000.0 1830.0 1; # W24X68
element elasticBeamColumn 21 15 16 20.1 29000.0 1830.0 1; # W24X68

# ---------------------------------
# Check Eigenvalues
# ---------------------------------

set eigenValues [eigen 5]

puts "\nEigenvalues:"
set eigenValue [lindex $eigenValues 0]
puts "T[expr 0+1] = [expr 2*$PI/sqrt($eigenValue)]"
set eigenValue [lindex $eigenValues 1]
puts "T[expr 1+1] = [expr 2*$PI/sqrt($eigenValue)]"
set eigenValue [lindex $eigenValues 2]
puts "T[expr 2+1] = [expr 2*$PI/sqrt($eigenValue)]"
set eigenValue [lindex $eigenValues 3]
puts "T[expr 3+1] = [expr 2*$PI/sqrt($eigenValue)]"
set eigenValue [lindex $eigenValues 4]
puts "T[expr 4+1] = [expr 2*$PI/sqrt($eigenValue)]"

recorder Node -file eigenvector.out -nodeRange 5 16 -dof 1 2 3 eigen 0
record

exit