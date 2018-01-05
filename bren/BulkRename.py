# Copyright (c) 2016, Michael Sonntag (sonntag@bio.lmu.de)
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted under the terms of the BSD License. See
# LICENSE file in the root of the project.

import os
import imghdr

__author__ = 'Michael Sonntag'


# TODO Add start and end
# TODO Add logfile
# TODO Add commandline support - add cmdline parser
# TODO Outsource program settings to JSON file, parse and read that in.

class BulkRename:

    def __init__(self):
        # Define the path of the main directory from which to rename files in folders.
        # main_dir_path = 'D:\\_Chaos\\DL\\handleImages\\testRename\\'
        self.main_dir_path = 'D:\\_Chaos\\Bilder\\201510_Zentralasien\\sorted\\'
        # Handle files in the main directory as well.
        self.include_main_dir = False
        # Define a base string that will be inserted into the renaming string.
        self.main_name = 'Zentralasien'
        # Use the name of the directory tree up to the main path when renaming a file.
        self.add_directory_name = True
        # Separator string that separates the part of the existing filename that will be
        # replaced with the part of the existing filename that will be kept
        # for the renaming string.
        self.name_separator = '__'
        # Define whether whitespace should be replaced or not.
        self.replace_white_space = True
        # White space separator, also used as white space replacement.
        self.white_space_separator = '_'
        # Define at which number the index for renaming multiple files in each folder
        # should start.
        self.batch_start_index = 1
        # Define if all files encountered in a directory should be renamed
        # or if only a defined subset should be subjected to renaming.
        self.rename_all_file_types = True
        # Define which types of files should be renamed.
        # TODO Current file type checks are really slow...
        self.rename_file_types = ['JPG', 'JPEG', 'PNG', 'GIF']
        # Define which directories within the main directory should be excluded
        # all together. This option is case sensitive.
        # exclude_dirs = ['excludeMe', '20150926_meToo']
        self.exclude_dirs = []

    def run(self):
        """
        Script used to batch rename files in a directory tree. At the moment only files
        in the first layer of subfolders will be taken into account.
        Files will be renamed in the following fashion:
        '[Subdirectory name]_[specified batch name]_[progressing index]__[part of the
        previous name after separator]'.
        The index will be reset for each subfolder, the starting index can be defined.
        It can be defined whether all files should be renamed, the renaming can also be
        restricted to specified file types only.
        Subdirectories can be excluded by name.
        """

        print("[Info] Starting ...")
        print("[Info] Handling folder %s; included: %s" %
              (self.main_dir_path, self.include_main_dir))
        print("[Info] MainName: %s; Add Directory Name: %s; batch start index: %s" %
              (self.main_name, self.add_directory_name, self.batch_start_index))
        print("[Info] Separator: '%s'; ws separator: '%s'; replace ws: '%s'" %
              (self.name_separator, self.white_space_separator, self.replace_white_space))
        print("[Info] Rename file types: %s" % self.rename_file_types)

        for path, dirs, files in os.walk(self.main_dir_path):
            if path != self.main_dir_path or self.include_main_dir:

                # TODO add better check for exclude_dirs at this point
                exclude_dir = False
                for curr_dir in self.exclude_dirs:
                    if path.find(curr_dir) > -1:
                        print("[Info] Directory " + curr_dir + " will be excluded")
                        exclude_dir = True

                if not exclude_dir:
                    split_dirs = [os.path.basename(path.rstrip('\\'))]
                    if path != self.main_dir_path:
                        split_path = os.path.abspath(path).replace(self.main_dir_path, '')
                        split_dirs = split_path.split('\\')

                    print("[Info] Process directory " + path)
                    i = self.batch_start_index
                    for f in files:
                        self.do_stuff(path, f, split_dirs, i)
                        i += 1

    def do_stuff(self, path, f, split_dirs, i):
        original_file = os.path.join(path, f)

        fpc = str(imghdr.what(original_file)).upper()
        if self.rename_all_file_types or self.rename_file_types.__contains__(fpc):
            if f.find(self.name_separator) == -1:
                print('[Warning] File "%s" does not contain separator' % f)
                # TODO Nicer filename integration into the print string.
                # TODO Check if this is a good way to handle the file
                # TODO ending when working with a missing name separator.
                split_parts = f.rsplit('.', 1)
                split_parts[1] = '.' + split_parts[1]
            else:
                split_parts = f.split(self.name_separator)

            file_name = ""

            # Add directory name to te current file name if set.
            # Make sure only one white space separator is used at the
            # end of the directory name.
            if self.add_directory_name:
                file_name += split_dirs[0].rstrip(self.white_space_separator)
                file_name += self.white_space_separator

            # TODO Check if inserting the main name into the first
            # directory and any subdirectory can be done in a better way.
            file_name += self.main_name + self.white_space_separator

            if self.add_directory_name:
                for d in split_dirs[1:]:
                    file_name += d.rstrip(self.white_space_separator)
                    file_name += self.white_space_separator

            file_name += "{:03d}".format(i)
            end_name = split_parts[1]
            if split_parts.__len__() > 2:
                for p in split_parts[2:]:
                    end_name += self.white_space_separator + p

            file_name.strip()
            end_name.strip()

            if self.replace_white_space & (file_name.find(' ') > 0):
                print("[Info] Replace white space in " + file_name)
                file_name = file_name.replace(' ', self.white_space_separator)
                file_name = file_name.replace(self.name_separator,
                                              self.white_space_separator)
            if self.replace_white_space & (end_name.find(' ') > 0):
                print("[Info] Replace white space in " + end_name)
                end_name = end_name.replace(' ', self.white_space_separator)
                end_name = end_name.replace(self.name_separator,
                                            self.white_space_separator)

            file_name += self.name_separator + end_name

            formatted_name = os.path.join(path, file_name)

            os.rename(original_file, formatted_name)
