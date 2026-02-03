#
#     Copyright (C) 2015 CCP-EM
#
#     This code is distributed under the terms and conditions of the
#     CCP-EM Program Suite Licence Agreement as a CCP-EM Application.
#     A copy of the CCP-EM licence can be obtained by writing to the
#     CCP-EM Secretary, RAL Laboratory, Harwell, OX11 0FA, UK.
#

'''
Example mrc i/o.
'''
import sys
import os
from PyQt4 import QtGui
import ccpem_core.gui.icons as icons
from ccpem_core.map_io import numpy_mrc_io
from ccpem_core import test_data
from ccpem_core.gui.image_viewer import gallery_viewer


def set_mrc(mrc_in_path):
        # Open mrc file
        header, data = numpy_mrc_io.read_mrc(mrc_in_path)
        # Write mrc file
        out_path = os.getcwd()
        mrc_out = os.path.join(out_path,
                               'test.mrcs')
        # Write mrc file
        data.setflags(write=True)
        data.fill(1.0)
        numpy_mrc_io.write_mrc(filename=mrc_out, header=header, data=data)
        # Example of numpy function
        print 'Shape : ', data.shape
        print 'Max   : ', data.max()
        print 'Alpha : ', header['alpha']
        print 'Xlen  : ', header['xlen']
        return mrc_out
        
        
def main():
    test_data_path = test_data.get_test_data_path()
    mrc_in_path = os.path.join(test_data_path,
                              'test.mrc')
    mrc_out_path = set_mrc(mrc_in_path)
    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(icons.icon_utils.get_ccpem_icon()))    
    mw = gallery_viewer.CCPEMGalleryWindow(
        filenames=[mrc_in_path, mrc_out_path])
    mw.show()
    app.exec_()
    sys.exit()

if __name__ == '__main__':
    main()

