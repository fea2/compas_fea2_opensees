wipe

model Basic -ndm 3 -ndf 3

set E 30000
set nu 0.2
set rho 2.5
set cubeSize 1.0

set Kn 1e6
set Kt 1e5
set mu 0.3
set G 10000
set c 50
set t 10

# Nodes for bottom cube
node 1 0.0 0.0 0.0
node 2 $cubeSize 0.0 0.0
node 3 $cubeSize $cubeSize 0.0
node 4 0.0 $cubeSize 0.0
node 5 0.0 0.0 $cubeSize
node 6 $cubeSize 0.0 $cubeSize
node 7 $cubeSize $cubeSize $cubeSize
node 8 0.0 $cubeSize $cubeSize

# Fix bottom cube
fix 1 1 1 1
fix 2 1 1 1
fix 3 1 1 1
fix 4 1 1 1

# Nodes for top cube
set zOffset [expr $cubeSize]
node 9 0.0 0.0 $zOffset
node 10 $cubeSize 0.0 $zOffset
node 11 $cubeSize $cubeSize $zOffset
node 12 0.0 $cubeSize $zOffset

# Mass for top cube nodes
set massPerNode [expr $rho*$cubeSize*$cubeSize*$cubeSize/8.0]
foreach node {9 10 11 12} {
    mass $node $massPerNode $massPerNode $massPerNode
}

# Contact material
nDMaterial ContactMaterial3D 1 $mu $G $c $t

# Lambda node for contact element
node 13 0.0 0.0 [expr $zOffset + 0.1]

# Tolerances
set tolGap 1e-3
set tolForce 1e-3

# Define a single contact element
element SimpleContact3D 1 5 6 7 8 9 13 1 $tolGap $tolForce

# Gravity load
set g -9.81
pattern Plain 1 Linear {
    foreach node {9 10 11 12} {
        load $node 0.0 0.0 [expr $massPerNode * $g]
    }
}

# Solver and analysis
system SparseSYM
numberer RCM
constraints Plain
integrator LoadControl 0.001
algorithm Newton
analysis Static

# Run analysis
set steps 1000
for {set i 0} {$i < $steps} {incr i} {
    if {[analyze 1] != 0} {
        puts "Analysis failed at step $i"
        break
    }
}

puts "Analysis Complete"