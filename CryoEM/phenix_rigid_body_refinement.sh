#!/usr/bin/bash


# Determine SSE in phenix.secondary_structure_restraints
phenix.secondary_structure_restraints protein.pdb format=phenix_refine

# Search for the word 'selection' and replace with 'group'
sed 's/selection/group/g' protein.pdb_ss.eff > intermediate.txt

# Grep each line in input file that has the word 'selection'
grep group intermediate.txt > protein.eff

# Add Phenix .eff format to first and last line
sed -e '1i\
	refinement.rigid_body {'  < protein.eff > rigid_groups.eff

sh -c "echo '}' >> rigid_groups.eff"

# Begin rigid-body refinement in phenix.real_space_refine
phenix.real_space_refine protein.pdb complete_map.mrc resolution=3.7 run=rigid_body rigid_groups.eff nproc=2

# Delete intermediate file
rm intermediate.txt protein.eff
