# ------------------------
# Basic_Truss_Example
# ------------------------
#
# None
#
#
# Author: None
# Description: None
# Date: 08/01/2025 12:32:28
# Generated by:
#   compas_fea2 v0.2.1
#   compas_fea2_opensees v0.1.0
#
#------------------------------------------------------------------
#------------------------------------------------------------------
# MODEL
#------------------------------------------------------------------
#------------------------------------------------------------------
#
##
# By default, models in compas_fea2 are defined in 3D.
model Basic -ndm 3
#
#==================================================================
# Materials
#==================================================================
#
uniaxialMaterial Elastic 0 3000.0
nDMaterial ElasticIsotropic 1000 3000.0 0.3 1.0
#
#==================================================================
# Sections
#==================================================================
#

#
#==================================================================
# Parts
#==================================================================
#
#
#------------------------------------------------------------------
# Part Truss
#------------------------------------------------------------------
model Basic -ndm 2 -ndf 2
#
# Nodes
#------------------------------------------------------------------
#
#    tag        X       Y       Z       mx      my      mz
node 0      0.00000000      0.00000000      0.00000000
node 1    144.00000000      0.00000000      0.00000000
node 2    168.00000000      0.00000000      0.00000000
node 3     72.00000000     96.00000000      0.00000000
#
# Elements
#------------------------------------------------------------------
#
element Truss 0 0 3 10.0 0
element Truss 1 1 3 5.0 0
element Truss 2 2 3 5.0 0
#
#
#
#
#------------------------------------------------------------------
# Initial conditions
#------------------------------------------------------------------
#
#    tag   DX   DY   RZ   MX   MY   MZ
fix 1 1 1
fix 2 1 1
fix 0 1 1
#
#
#------------------------------------------------------------------
# Connectors
#------------------------------------------------------------------
#

#
#
#
#
# -----------------------------------------------------------------
# -----------------------------------------------------------------
# PROBLEM
# -----------------------------------------------------------------
# -----------------------------------------------------------------
#
##
#
# STEP StaticStep
#
timeSeries Constant 0 -factor 1.0
#
# - Displacements
#   -------------
#
#
# - Loads
#   -----
pattern Plain 0 0 -fact 1 {
	load 3 100.0 -50.0
}
#
# - Predefined Fields
#   -----------------
#
#
#
# - Analysis Parameters
#   -------------------
#
constraints Transformation 
numberer RCM
system BandGeneral    
test NormDispIncr 1.0e-6 10
algorithm Newton
integrator LoadControl 1
analysis Static

analyze 1
# loadConst -time 0.0
#
# - Output Results
#   --------------
#

# ---------------------------------------------
# Custom Displacement Export Script
# ---------------------------------------------
set dispFile [open "u.out" "w"]
set allNodes [getNodeTags]
foreach nodeTag $allNodes {
    set disp [nodeDisp $nodeTag]
    puts $dispFile "$nodeTag $disp"
}
close $dispFile
puts "Displacements have been exported to u.out"

#
