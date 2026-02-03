#!/usr/bin/python

import os
import numpy as np
import mrcfile

# Remove the previously written file:
os.remove('tmp.mrc')

# First create a simple dataset:
example_data=np.arange(12,dtype=np.int8).reshape(3,4)

# Make a new MRC file and write to it:
with mrcfile.new('tmp.mrc') as mrc:
    mrc.set_data(example_data)

# The file is now saved to disk.
# Open it again and check the data:
with mrcfile.open('tmp.mrc') as mrc:
    mrc.data

# Close the file:
mrc.close()
