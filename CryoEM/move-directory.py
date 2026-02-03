#!/usr/bin/python

"""
A program to move directories to a different location and place a symbolic link at the old location pointing to the
new location.

This scenario will use a source directory with the path /some/src/path/dir and a destination of
/some/dest/path.

python move-directory.py /some/src/path/dir /some/dest/path

Assuming the path to the directory is /some/src/path/dir the program
would calculate the SHA256 checksums of all the files within the directory /some/src/path/dir and write the
checksums to the file /some/src/path/dir/dir.sha256.  Once this is complete the program will copy the
contents of /some/src/path/dir into a destination directory /some/dest/path/dir and copy the checksum file from
/some/src/path/dir/dir.sha256 to /some/dest/path/dir/dir.sha256.
Then it would verify the copied file checksums using the checksum file that now exists at
/some/dest/path/dir/dir.sha256.  If all the checksums are the same the program will delete the
directory /some/src/path/dir.  It would then place a symbolic link at /some/src/path/dir pointing to the
/some/dest/path/dir directory.
"""

import os
import sys
import argparse
import ConfigParser
import hashlib
from distutils.dir_util import (mkpath, remove_tree, create_tree, copy_tree, ensure_relative)
import logging


def get_options():
    """
    Options parser using the argparse library.

    :return arguments:
    """
    parser = argparse.ArgumentParser(description="""
A program to move a directory to a different location, verify checksums, 
remove the original directory, and place a symbolic link at the old directory 
path pointing to the new directory path.

This program copies symbolic links as symbolic links!  It will not copy the 
target of the symbolic links nor will it correct relative symbolic links.
Symbolic links that have the absolute path will still function as expected.

Example:
This scenario will use a directory name of /some/src/path/dir and a destination
of /some/dest/path/dir.

$ python move-directory.py /some/src/path/dir /some/dest/path/dir

Assuming the directory path is /some/src/path/dir the 
program would calculate the SHA256 checksums of all the files within the 
directory /some/src/path/dir and write the checksums to the file 
/some/src/path/dir.sha256.

Once this was complete the program will copy the contents of 
/some/src/path/dir into a destination directory 
/some/dest/path/dir.

Then it would verify the copied file checksums using the checksum file that 
was copied to /some/dest/path/dir.sha256.

If all the checksums match the program would delete the directory 
/some/src/path/dir.

It would then place a symbolic link at /some/src/path/dir pointing to 
the /some/dest/path/dir directory.

To verify the /some/src/path/dir is actually a symbolic link to 
/some/dest/path/dir you may use the file program to interrogate
the /some/src/path/dir object by doing the following (without the $):

$ file /some/src/path/dir

If the item in question is a symbolic link the program will return something
like this:
/some/src/path/dir: symbolic link to '/some/dest/path/dir'

If the object in question is a directory the program will return something
like this:
/some/src/path/dir: directory
    """, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('source', action='store', type=str,
                        help='The full path to the directory you would like moved.')
    parser.add_argument('destination', action='store', type=str,
                        help='The full path to the directory you would like the source directory moved to.')
    parser.add_argument('-n', '--dry-run', action='store_true', default=False, dest='dry_run',
                        help='Show what would be done but do not make any changes.')
    # parser.add_argument('-l', '--logfile', action='store', type=str, dest='logfile',
    #                     help='The path to the file you would like the output written to.')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, dest='verbose',
                        help='Enable verbose output.')
    parser.add_argument('-vv', '--debug', action='store_true', default=False, dest='debug',
                        help='Enable debug output.')
    arguments = parser.parse_args()
    return arguments


def config_logger():
    """
    Configure the logger.
    """
    if options.logfile is not None:
        # create logger with 'move_frames'
        logger = logging.getLogger('move_frames')
        if options.debug is True:
            # Set the logging level to DEBUG
            logger.setLevel(logging.DEBUG)
        elif options.verbose is True:
            # Set the logging level to INFO
            logger.setLevel(logging.INFO)
        elif options.verbose is False and options.debug is False:
            # Set the logging level to ERROR
            logger.setLevel(logging.ERROR)
        # create file handler
        fh = logging.FileHandler(options.logfile)
        fh.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(fh)
        logger.addHandler(ch)


def validate_path(path):
    """
    Validates the path passed into the function exists, is not a symbolic link,
    and is writable.  If one of those is not true it will raise an exception.
    If no issues are encountered the function returns the path.

    :param path:
    :type path: str

    :return path:
    :rtype path: str
    """
    if options.debug is True:
        print('Validating path: {}\n'.format(path))
    if not isinstance(path, str) or not path:
        print('ERROR {} is not a string or is not set'.format(path))
        raise SystemExit('{} is not a string or is not set.'.format(path))
    if not os.path.isdir(path):
        print('ERROR {} is not a valid directory.'.format(path))
        raise SystemExit('{} is not a valid directory.'.format(path))
    elif os.path.islink(path):
        print('ERROR {} is a symbolic link.'.format(path))
        raise SystemExit('{} is a symbolic link'.format(path))
    elif not os.access(path, os.W_OK):
        print('ERROR {} is not writable.'.format(path))
        raise SystemExit('{} is not writable.'.format(path))
    if options.debug is True:
        print('Path {} has been validated'.format(path))
    return path


def destination_path(dest, src_path):
    """
    Given the path to the source directory create the path to the destination
    directory where the files will be copied to.

    :param dest:
    :param src_path:
    :return:
    """
    if options.debug is True:
        print('Entering the destination_path function.')
    # Given the src_path '/some/src/path/dir'
    # parent_path is '/some/src/path'
    # data_dir is 'dir'
    parent_path, data_dir = os.path.split(src_path)
    # Given a dest path on the command line of /some/dest/path then this
    # dest_path would be /some/dest/path/dir
    dest_path = os.path.join(dest, data_dir)
    if options.debug is True:
        print('The destination_path function returned: {}'.format(dest_path))
        print('Exiting the destination_path function.')
    return dest_path


def enumerate_files(dir_path):
    """
    Retrieves all the files in the directory specified.

    :param dir_path:
    :type dir_path: str

    :return file_list:
    :rtype list

    """
    if options.debug is True:
        print("Entering the enumerate_files function.")
        print('Enumerating files in the directory: {}'.format(dir_path))
    if options.verbose is True:
        print('Enumerating files in the directory: {}'.format(dir_path))
    file_list = list()
    for root, dirs, files in os.walk(dir_path):
        for f in files:
            # if options.debug is True:
            #     print '{}'.format(os.path.join(root, f))
            full_file_path = os.path.join(root, f)
            file_list.append(full_file_path)
    if options.debug is True:
        print('Exiting the enumerate_parent_files function.')
    return file_list


def compute_checksum(path, blocksize=65536):
    """
    Given a list of files this will calculate the SHA256SUM for each file.  The file and its checksum are then entered
    into a dictionary where the key is the file and the value is the checksum.  The return object is the created
    dictionary.

    :param blocksize: Specify how many bytes of the file you want to open at a time
    :param path:

    :return checksum:
    :rtype: str
    """

    hasher = hashlib.sha256()
    with open(path, 'rb') as target:
        buff = target.read(blocksize)
        while len(buff) > 0:
            hasher.update(buff)
            buff = target.read(blocksize)
    checksum = hasher.hexdigest()
    return checksum


def write_checksum_file(src_path, checksum_dict):
    """
    Given a path to a directory (src_path) and a dictionary object (checksum_dict) create a text file with the
    checksums and relative file paths.  We are assuming this is a SHA256 checksum so we append .sha256 to the file name.
    The checksum file is named for the parent directory of src_path and contains on each line a checksum then the
    relative path to the file using the parent_directory of src_path as the starting point.

    Given a src_path of /some/src/path/dir and two files within the dir directory:
    /some/src/path/dir/a.file
    /some/src/path/dir/dira/b.file

    The checksum file will be created at /some/src/path/dir/dir.sha256 with the contents:
    some_unique_checksum_string a.file
    some_unique_checksum_string dira/b.file

    The checksum_file_path is returned and in this example the returned value would be
    /some/src/path/dir/dir.sha256

    :param src_path:
    :type src_path: str

    :param checksum_dict:
    :type checksum_dict: dict

    :return checksum_file_path:
    :rtype: str
    """
    if options.debug is True:
        print('Entering the write_checksum_file function.')
    if options.verbose is True:
        print('Writing out the checksum file.')
    checksum_file_path = os.path.join(os.path.join(src_path, os.path.basename(src_path) + '.' + 'sha256'))
    relative_dir = os.path.dirname(checksum_file_path)
    with open(checksum_file_path, 'w') as f:
        for key in checksum_dict:
            f.write('{} {}\n'.format(key, os.path.relpath(checksum_dict[key], relative_dir)))
    if options.debug is True:
        print('Leaving the write_checksum_file function.\nThe function returned {}'.format(checksum_file_path))
    return checksum_file_path


def copy_files(src, dst):
    """
    Copy files within the src directory into the dst directory.

    :param src:
    :type src: str

    :param dst:
    :type src: str

    :return output_files:
    :rtype: list
    """
    # copy_tree(src, dst[, preserve_mode=1, preserve_times=1, preserve_symlinks=0, update=0, verbose=0, dry_run=0])
    # If src is /some/src/path/dir and dst is /some/dest/path the files and dirs in
    # /some/src/path/dir will be copied into /some/dest/path
    if options.debug is True:
        print('Entering the copy_files function.')
        print('The provided arguments are:\nsrc: {}\ndst: {}'.format(src, dst))
    if options.verbose is True:
        verbose_opt = 1
    else:
        verbose_opt = 0

    if options.dry_run is True:
        dry_run_opt = 1
    else:
        dry_run_opt = 0
    if options.debug is True:
        print('The copy_tree command is being run as follows:\ncopy_tree({}, {}, preserve_mode=1, preserve_times=1, ' \
              'preserve_symlinks=1, update=0, verbose={}, dry_run={})'.format(src, dst, verbose_opt, dry_run_opt))
    output_files = copy_tree(src, dst, preserve_mode=1, preserve_times=1, preserve_symlinks=1, update=0,
                             verbose=verbose_opt, dry_run=dry_run_opt)

    return output_files


def verify_checksums_from_file(file_path, blocksize=65536):
    """
    Given the path to a checksum file containing SHA256 checksums, compute the SHA256 checksum of each file then check
    to see if the computed checksum is the same as the one in the file.
    If the checksums are not the same raise an error.

    :param file_path:
    :type file_path: str

    :param blocksize:
    :type blocksize: int

    :return:
    """
    if options.debug is True:
        print('Entering the verify_checksums_from_file function.')
        print('The file_path argument is {}'.format(file_path))
        print('The blocksize argument is {}'.format(blocksize))
    base_dir = os.path.dirname(file_path)
    orig_dir = os.getcwd()
    # Change to the directory containing the checksum_file because the file paths are relative
    os.chdir(base_dir)
    if options.debug is True:
        print('Currently in the directory {}'.format(os.getcwd()))
    checksums = dict()
    with open(file_path, 'r') as fp:
        for line in fp:
            checksum, target = line.strip().split(' ')
            if options.debug is True:
                print('The checksum of the target {} is: {}'.format(checksum, target))
            # The sha256sum is the key and the path is the value.
            checksums[checksum] = target
    for key in checksums.keys():
        # Initialize the hashlib object each time so we start fresh.
        hasher = hashlib.sha256()
        # Verify the file exists
        if os.path.isfile(checksums.get(key)):
            with open(checksums.get(key), 'rb') as f:
                buff = f.read(blocksize)
                while len(buff) > 0:
                    hasher.update(buff)
                    buff = f.read(blocksize)
                sys.stdout.flush()
            # Check if the computed sha256sum is the same as the sha256sum from the file.
            if hasher.hexdigest() == key:
                if options.verbose is True:
                    print('{}: OK'.format(checksums.get(key)))
            else:
                raise Exception('The checksums for the file:\n{}\ndoes not match!'.format(file_path))
        else:
            # print 'The file {} does not exist.'.format(checksums.get(key))
            raise Exception('The file {} does not exist.'.format(checksums.get(key)))
    # Return to the directory the program was called in
    os.chdir(orig_dir)

    return


def remove_source_files(target):
    """
    Remove the directory at target and everything below it.

    :param target: Path to target directory
    :type target: str

    :return:
    """
    if options.verbose is True:
        print('Removing {} (and everything under it).'.format(target))

    if options.verbose is True:
        verbose_opt = 1
    else:
        verbose_opt = 0

    if options.dry_run is True:
        dry_run_opt = 1
    else:
        dry_run_opt = 0

    remove_tree(target, verbose=verbose_opt, dry_run=dry_run_opt)

    return


def symlink_to_dest(src, dest):
    """
    Creates a symbolic link at the dest path that points to the src path.  It then verifies the symbolic links exists
    and if it does not it throws an exception to the user.

    :param src:
    :type src: str

    :param dest:
    :type dest: str

    :return:
    """

    os.symlink(src, dest)

    if not os.path.islink(dest):
        raise Exception('Unable to create symbolic link {} pointing at {}.'.format(dest, src))

    return


def main():
    """
    Main execution of the program.
    """
    if options.dry_run is True:
        print('Performing a dry run.  Nothing will be done, but what would be done will be printed to the console.')
    # Validate that the source path exists, is a directory, not a symbolic link, and writable
    validate_path(options.source)
    # Validate that the destination path exists, is a directory, not a symbolic link, and writable
    validate_path(options.destination)
    # Given a destination path of /some/dest/path and a source path of /some/src/path/dir
    # The dest_path will be /some/dest/path/dir
    dest_path = destination_path(options.destination, options.source)
    # A list of all files found in /some/src/path/dir
    files = enumerate_files(options.source)
    if options.dry_run is True:
        print('\nWould copy {} files.'.format(len(files)))
        print('\nThe files that would be copied are:')
        print('\n'.join(files))
        copied_files = copy_files(options.source, dest_path)
        print '\nThe resulting files would be:'
        print('\n'.join(copied_files))
    else:
        if options.verbose is True:
            print 'Beginning to compute checksums on {} files.'.format(len(files))
        checksums = dict()
        count = 0
        for f in files:
            count += 1
            sys.stdout.write('\r')
            sys.stdout.write('Calculating checksum {} of {}'.format(count, len(files)))
            sys.stdout.flush()
            # Verify the file exists.
            if os.path.isfile(f):
                # The dictionary is {'checksum': 'file_path',}
                checksums[compute_checksum(f)] = f
            elif os.path.islink(f):
                # Don't try to compute a checksum for symbolic links because of potential issues
                pass
            else:
                # sys.stdout.write does not include a new line character at the end of the output like print does
                sys.stdout.write('\n')
                raise Exception('{} is not a valid file'.format(f))
        # sys.stdout.write does not include a new line character at the end of the output like print does
        sys.stdout.write('\n')
        # Create the checksum file
        path_to_checksum_file = write_checksum_file(options.source, checksums)
        if options.verbose is True:
            print 'The file containing the checksums is {}.'.format(path_to_checksum_file)
        # Copy the files
        copied_files = copy_files(options.source, dest_path)
        verify_checksums_from_file(os.path.join(dest_path, os.path.basename(options.source) + '.' + 'sha256'))
        # The checksums have been verified and we can now remove the source files.
        remove_source_files(options.source)
        if os.path.isdir(options.source):
            print 'An error occurred, the directory {} should not still exist.'.format(options.source)
            raise Exception('The directory {} was not removed.'.format(options.source))
        print 'Creating a symbolic link at {} pointing to {}'.format(options.source, dest_path)
        os.symlink(dest_path, options.source)


if __name__ == "__main__":
    # config = get_config()
    options = get_options()
    # log = config_logger()
    main()
