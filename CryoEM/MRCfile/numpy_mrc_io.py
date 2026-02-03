#
#     Copyright (C) 2015 CCP-EM
#
#     This code is distributed under the terms and conditions of the
#     CCP-EM Program Suite Licence Agreement as a CCP-EM Application.
#     A copy of the CCP-EM licence can be obtained by writing to the
#     CCP-EM Secretary, RAL Laboratory, Harwell, OX11 0FA, UK.
#


import os
import numpy as np
from os import stat
from struct import unpack_from
import sys
from ccpem_core import test_data
from PyQt4.Qt import QImage

'''
    Axes conversions
    MAPC            Which axis corresponds to Cols.  (1,2,3 for X,Y,Z) [fast]
    MAPR            Which axis corresponds to Rows   (1,2,3 for X,Y,Z)
    MAPS            Which axis corresponds to Sects. (1,2,3 for X,Y,Z) [slow]
    #
    Numpy arrays always stored as row-major [slow z | y | x fast].
'''

mrc_axis = {'x': 1,
            'y': 2,
            'z': 3}
np_axis =  {'x': 2,
            'y': 1,
            'z': 0}


def create_header_dtype(byte_order='='):
    '''
    Numpy byte order
        '='    native
        '<'   little-endian
        '>'    big-endian
        '|'    not applicable
    '''
    rec_header_dtd = \
    [
        ['nx', 'i4'],              # Number of columns
        ['ny', 'i4'],              # Number of rows
        ['nz', 'i4'],              # Number of sections

        ['mode', 'i4'],            # Types of pixels in the image. Values used by IMOD:
                                   #  0 = unsigned or signed bytes depending on flag in imodFlags
                                   #  1 = signed short integers [16 bits]
                                   #  2 = float [32 bits]
                                   #  3 = short * 2, [used for complex data]
                                   #  4 = float * 2, [used for complex data]
                                   #  6 = unsigned 16-bit integers [non-standard]
                                   # 16 = unsigned char * 3 [for rgb data, non-standard]

        ['nxstart', 'i4'],         # Starting point of sub-image [not used in IMOD]
        ['nystart', 'i4'],
        ['nzstart', 'i4'],

        ['mx', 'i4'],              # Grid size in X, Y and Z
        ['my', 'i4'],
        ['mz', 'i4'],

        ['xlen', 'f4'],            # Cell size; pixel spacing = xlen/mx, ylen/my, zlen/mz
        ['ylen', 'f4'],
        ['zlen', 'f4'],

        ['alpha', 'f4'],           # Cell angles - ignored by IMOD
        ['beta', 'f4'],
        ['gamma', 'f4'],

        # These need to be set to 1, 2, and 3 for pixel spacing to be interpreted correctly
        ['mapc', 'i4'],            # map column  1=x,2=y,3=z.
        ['mapr', 'i4'],            # map row     1=x,2=y,3=z.
        ['maps', 'i4'],            # map section 1=x,2=y,3=z.

        # These need to be set for proper scaling of data
        ['amin', 'f4'],            # Minimum pixel value
        ['amax', 'f4'],            # Maximum pixel value
        ['amean', 'f4'],           # Mean pixel value

        ['ispg', 'i4'],            # space group number [ignored by IMOD]
        ['next', 'i4'],            # number of bytes in extended header [called nsymbt in MRC standard]
        ['creatid', 'i2'],         # used to be an ID number, is 0 as of IMOD 4.2.23
        ['extra_data', 'V30'],     # [not used, first two bytes should be 0]

        # These two values specify the structure of data in the extended header; their meaning depend on whether the
        # extended header has the Agard format, a series of 4-byte integers then real numbers, or has data
        # produced by SerialEM, a series of short integers. SerialEM stores a float as two shorts, s1 and s2, by:
        # value = [sign of s1]*[|s1|*256 + [|s2| modulo 256]] * 2**[[sign of s2] * [|s2|/256]]
        ['nint', 'i2'],            # Number of integers per section [Agard format] or number of bytes per section [SerialEM format]
        ['nreal', 'i2'],           # Number of reals per section [Agard format] or bit
                                   # Number of reals per section [Agard format] or bit
                                   # flags for which types of short data [SerialEM format]:
                                   # 1 = tilt angle * 100  [2 bytes]
                                   # 2 = piece coordinates for montage  [6 bytes]
                                   # 4 = Stage position * 25    [4 bytes]
                                   # 8 = Magnification / 100 [2 bytes]
                                   # 16 = Intensity * 25000  [2 bytes]
                                   # 32 = Exposure dose in e-/A2, a float in 4 bytes
                                   # 128, 512: Reserved for 4-byte items
                                   # 64, 256, 1024: Reserved for 2-byte items
                                   # If the number of bytes implied by these flags does
                                   # not add up to the value in nint, then nint and nreal
                                   # are interpreted as ints and reals per section

        ['extra_data2', 'V20'],    # extra data [not used]

        ['imodStamp', 'i4'],       # 1146047817 indicates that file was created by IMOD
        ['imodFlags', 'i4'],       # Bit flags: 1 = bytes are stored as signed

        # Explanation of type of data
        ['idtype', 'i2'],          # [ 0 = mono, 1 = tilt, 2 = tilts, 3 = lina, 4 = lins]
        ['lens', 'i2'],
        ['nd1', 'i2'],             # for idtype = 1, nd1 = axis [1, 2, or 3]
        ['nd2', 'i2'],
        ['vd1', 'i2'],             # vd1 = 100. * tilt increment
        ['vd2', 'i2'],             # vd2 = 100. * starting angle

        # Current angles are used to rotate a model to match a new rotated image.  The three values in each set are
        # rotations about X, Y, and Z axes, applied in the order Z, Y, X.
        ['triangles', 'f4', 6],    # 0,1,2 = original:  3,4,5 = current

        ['xorg', 'f4'],            # Origin of image
        ['yorg', 'f4'],
        ['zorg', 'f4'],

        ['cmap', 'S4'],            # Contains 'MAP '
        ['stamp', 'u1', 4],        # First two bytes have 17 and 17 for big-endian or 68 and 65 for little-endian

        ['rms', 'f4'],             # RMS deviation of densities from mean density

        ['nlabl', 'i4'],           # Number of labels with useful data
        ['labels', 'S80', 10]      # 10 labels of 80 characters
    ]
    # Set byte order for each data type, convert to tuple.
    for n in xrange(len(rec_header_dtd)):
        l = rec_header_dtd[n]
        l[1] = byte_order + l[1]
        rec_header_dtd[n] = tuple(l)
    rec_header_dtype = np.dtype(rec_header_dtd)
    assert rec_header_dtype.itemsize == 1024
    return rec_header_dtype


def read_mrc(filename,
             header_only=False,
             header_unprocessed_data=False,
             verbose=False):
    '''
    Read MRC map file.
    header_only = return header only
    '''
    assert [header_only, header_unprocessed_data].count(True) < 2
    # Read machine stamp to get byte order
    # Machine stamp as defined:
    # http://www.ccp4.ac.uk/html/maplib.html
    header = file(filename).read(1344)
    stamp = [unpack_from('B', header, 53*4+n)[0] for n in range(4)]
    del header
    if (stamp[0] == 68 and stamp[1] == 65)\
        or (stamp[0] == 68 and stamp[1] == 68)\
            or (stamp[3] == 68 and stamp[4] == 65): # For old chimera bug
                byte_order = '<'
    else:
        byte_order = '>'

    # Read header
    rec_header_dtype = create_header_dtype(byte_order=byte_order)
    fd = open(filename, 'rb')
    stats = stat(filename)
    hdr_str = fd.read(rec_header_dtype.itemsize)
    header = np.ndarray(shape=(), dtype=rec_header_dtype, buffer=hdr_str)
    header.setflags(write=True)
    if verbose:
        print_header(header=header)

    # Seek extended header
    if header['next'] > 0:
        fd.seek(rec_header_dtype.itemsize + header['next'])  # ignore extended header

    # Return header only
    if header_only:
        return header

    # Return header for editing and unprocessed binary data.
    # e.g. for repairing damaged headers.
    if header_unprocessed_data:
        data = fd.read()
        return header, data

    mode = header['mode']
    sign = 'i1' if header['imodFlags'] == 1 else 'u1' # signed or unsigned
            # 0     1     2     3     4    5     6     7     8     9     10    11    12    13    14    15    16
    dtype = [sign, 'i2', 'f',  'c4', 'c8', None, 'u2', None, None, None, None, None, None, None, None, None, 'u1'][mode]
    dsize = [ 1,    2,    4,    4,    8,   0,    2,    0,    0,    0,    0,    0,    0,    0,    0,    0,    3][mode]

    # data dimensions
    nx, ny, nz = header['nx'], header['ny'], header['nz']
    img_size = nx * ny * nz * dsize
    img_str = fd.read(img_size)
    dtype = byte_order + dtype

    # Make sure that we have read the whole file
    assert not fd.read()
    assert stats.st_size == header.itemsize + img_size
    fd.close()

    # Set axes order
    shape = range(3)
    mrc_to_numpy = {1: 2,
                    2: 1,
                    3: 0}
    shape[mrc_to_numpy[int(header['mapc'])]] = nx
    shape[mrc_to_numpy[int(header['mapr'])]] = ny
    shape[mrc_to_numpy[int(header['maps'])]] = nz
    if mode == 16:
        shape.append(3)

    # Read data
    data = np.ndarray(shape=shape, dtype=dtype, buffer=img_str)
    # Correct axes order if not x=sec, y=row, z=col
    axes = [mrc_to_numpy[int(header['maps'])],
            mrc_to_numpy[int(header['mapr'])],
            mrc_to_numpy[int(header['mapc'])]]
    if axes != [0, 1, 2]:
        if mode == 16:
            axes.append(4)
        data = data.transpose(axes).copy(order='C')
    return header, data


def print_header(header):
    for item in header.dtype.names:
        print '{0:15s} : {1}'.format(item, header[item])


def write_mrc(filename, header, data, map_col='y', map_row='x', map_sec='z'):
    '''
    Write mrc file.
    '''
    # Set all header infomation
    assert map_col in mrc_axis.keys()
    assert map_row in mrc_axis.keys()
    assert map_sec in mrc_axis.keys()
    assert map_col != map_row != map_sec
    # Set header
    header['mapc'] = mrc_axis[map_col]
    header['mapr'] = mrc_axis[map_row]
    header['maps'] = mrc_axis[map_sec]
    header['amin'] = data.min()
    header['amax'] = data.max()
    header['amean'] = data.mean()
    header['rms'] = data.std()
    # To do -> set other info

    # Set numpy axis
    set_axis = (np_axis[map_sec], np_axis[map_row], np_axis[map_col])
    if set_axis != (0, 1, 2):
        data = data.transpose(set_axis).copy(order='C')
    # Set machine stamp
    if sys.byteorder == 'little':
        header['stamp'] = (68, 65, 0, 0)
    else:
        header['stamp'] = (17, 17, 0, 0)
    write_raw_mrc(filename=filename, header=header, data=data)


def write_raw_mrc(filename, header, data):
    # Write file
    f = open(filename, 'wb')
    f.write(header)
    f.write(data)
    f.close()