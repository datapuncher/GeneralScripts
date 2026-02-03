Shift CryoEM Maps to the Origin
--------------------------------------------
# ChimeraX (command line interpreter)      #
# You can also use the resampling option   #
# if an already centered map is available  #
--------------------------------------------

$ volume #1 origin 0,0,0

-----------------------------------------------
# EMAN2 (from Python interpreter)             #
# First invoke the python interpreter and     #
# load the EMAN2 modulefrom the command line. #
-----------------------------------------------

$ module load eman2
$ python3

1. >>> from EMAN2 import *
2. >>> map=EMData('map_to_load.mrc')
3. >>> map['origin_x']=0
4. >>> map['origin_y']=0
5. >>> map['origin_z']=0
6. >>> map.write_image('map_cent.mrc')

# Explanation of code for each line:
1. import EMAN2 module
2. Load map to be shifted
3. Set origin of X axis
4. Set origin of Y axis
5. Set origin of Z axis
6. Write out new map

----------------------------------------------
#                   PyEM                     #
# PyEM installation instructions included    #
# You might need to use the --apix option    #
----------------------------------------------

$ conda install -c conda-forge pyem
$ map.py --origin x,y,z map.mrc map_cent.mrc
000000000
----------------------------------------------
#                    PHENIX                  #
# From the command line                      #
----------------------------------------------

$ phenix.map_box input_map.mrc keep_map_size=True prefix=origin_shifted output_origin_grid_units=0,0,0 output map = origin_shifted.ccp4
CCPEM

----------------------------------------------
#                   CCPEM                    #
# From the command line                      #
# Although you can do this by using          #
# the 'MapProcess' program in the GUI        #
----------------------------------------------

$ ccpem-python map_preprocess.pyc -m  input_map.mrc -l shift_origin -ori 0.0 0.0 0.0
