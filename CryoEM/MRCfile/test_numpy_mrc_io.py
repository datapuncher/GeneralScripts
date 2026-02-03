#
#     Copyright (C) 2015 CCP-EM
#
#     This code is distributed under the terms and conditions of the
#     CCP-EM Program Suite Licence Agreement as a CCP-EM Application.
#     A copy of the CCP-EM licence can be obtained by writing to the
#     CCP-EM Secretary, RAL Laboratory, Harwell, OX11 0FA, UK.
#

'''
Test mrc i/o.
'''

import unittest
import os
import shutil
import numpy as np
import tempfile
import numpy_mrc_io
from ccpem_core import ccpem_utils
from ccpem_core import test_data


class MrcIOTest(unittest.TestCase):
    '''
    Unit test for MRC i/o.
    '''
    def setUp(self):
        self.test_data = test_data.get_test_data_path()
        self.test_output = tempfile.mkdtemp()

    def tearDown(self):
        if os.path.exists(self.test_output):
            shutil.rmtree(self.test_output)

    def test_mrc_io(self):
        '''
        Test read/write.
        '''
        ccpem_utils.print_header(message='Unit test - MRC python i/o')
        # Open mrc file
        mrc_in = os.path.join(self.test_data,
                              'test.mrc')
        header, data = numpy_mrc_io.read_mrc(mrc_in)
        # Check max
        self.assertAlmostEqual(data.max(),
                               87175.8,
                               1)
        # Check array order
        self.assertAlmostEqual(data[0][0][0],
                               72171.2,
                               1)
        self.assertAlmostEqual(data[0][1][0],
                               69786.5,
                               1)
        self.assertAlmostEqual(data[0][-1][-1],
                               70929.9,
                               1)
        # Write mrc file
        mrc_out = os.path.join(self.test_output,
                               'test.mrcs')
        # Re-open mrc file
        numpy_mrc_io.write_mrc(filename=mrc_out, header=header, data=data)
        header, data = numpy_mrc_io.read_mrc(mrc_out)
        mrc_in = os.path.join(self.test_data,
                              'map/mrc/1ake_4-5A.mrc')
        header = numpy_mrc_io.read_mrc(mrc_in, header_only=True)
        assert header['alpha'] == 90.0
        assert header['xlen'] == 75.0

    def test_add_noise_to_volume(self, verbose=False):
        ccpem_utils.print_header(message='Unit test - Add noise volume')

        def print_data_stats(data):
            if verbose:
                print data.mean()
                print data.min()
                print data.max()
                print data.shape
        # Test load and save volume
        mrc_in = os.path.join(self.test_data,
                              'map/mrc/1ake_4-5A.mrc')
        header, data = numpy_mrc_io.read_mrc(mrc_in)
        print_data_stats(data=data)
        mrc_out = os.path.join(self.test_output,
                               'test_out.mrc')
        numpy_mrc_io.write_mrc(filename=mrc_out, header=header, data=data)
        # Load volume and add noise via numpy
        del header, data
        header, data = numpy_mrc_io.read_mrc(mrc_out)
        print_data_stats(data=data)
        noise = np.random.normal(loc=1,
                                 scale=0.1,
                                 size=[50, 50, 50]).astype(data.dtype)
        data_noise = data * noise
        print_data_stats(data=data_noise)
        noise_out = os.path.join(self.test_output,
                                 '1ake_4-5A_noise.mrc')
        numpy_mrc_io.write_mrc(filename=noise_out,
                               header=header,
                               data=data_noise)

if __name__ == '__main__':
    unittest.main()
