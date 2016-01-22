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


# TODO add start and end
# TODO add logfile
# TODO add commandline support - add cmdline parser and optional reading of JSON argument file
# TODO add tests

class Main:
    def run(self):
        """
        Script used to batch rename files in a directory tree. At the moment only files in the
        first layer of subfolders will be taken into account.
        Files will be renamed in the following fashion:
        '[Subdirectory name]_[specified batch name]_[progressing index]__[part of the previous name after separator]'.
        The index will be reset for each subfolder, the starting index can be defined.
        It can be defined whether all files should be renamed, the renaming can also be restricted to
        specified file types only.
        Subdirectories can be excluded by name.
        """
        # Define the path of the main directory from which to rename files in folders.
        main_dir_path = 'D:\\_Chaos\\Bilder\\201510_Zentralasien\\testRename\\'
        # Define a base string that will be inserted into the renaming string.
        main_name = 'Zentralasien'
        # Use the name of the directory when renaming a file.
        add_directory_name = True
        # Separator string that separates the part of the existing filename that will be
        # replaced with the part of the existing filename that will be kept for the renaming string.
        name_separator = '__'
        # Define whether whitespace should be replaced or not.
        replace_white_space = True
        # White space separator, also used as white space replacement.
        white_space_separator = '_'
        # Define at which number the index for renaming multiple files in each folder should start.
        batch_start_index = 1
        # Define if all files encountered in a directory should be renamed
        # or if only a defined subset should be subjected to renaming.
        rename_all_file_types = True
        # Define which types of files should be renamed.
        rename_file_types = ['JPG', 'JPEG', 'PNG']
        # Define which directories within the main directory should be excluded all together.
        # This is case sensitive.
        exclude_dirs = ['excludeMe', '20150926_meToo']

        for path, dirs, files in os.walk(main_dir_path):
            if path != main_dir_path:

                # TODO add better check for exclude_dirs at this point
                do_exclude = False
                for curr_dir in exclude_dirs:
                    if path.find(curr_dir) > -1:
                        print("[Info] Directory " + curr_dir + " will be excluded")
                        do_exclude = True

                if not do_exclude:
                    print("[Info] Process directory " + path)
                    i = batch_start_index
                    for f in files:
                        original_file = os.path.join(path, f)

                        if rename_all_file_types or rename_file_types.__contains__(str(imghdr.what(original_file)).upper()):
                            if not f.find(name_separator) > -1:
                                # TODO integrate filename in a nicer way into the print string
                                print("[Warning] File \'" + f + "\' does not contain separator")
                            else:
                                split_parts = f.split(name_separator)

                                file_name = ""

                                # Add directory name to te current file name if set.
                                # Make sure only one white space separator is used at the
                                # end of the directory name.
                                if add_directory_name:
                                    file_name = os.path.basename(path).rstrip(white_space_separator)
                                    file_name += white_space_separator

                                file_name += main_name + white_space_separator
                                file_name += "{:03d}".format(i)
                                file_name += name_separator + split_parts[1]

                                file_name.strip()

                                if replace_white_space & (file_name.find(' ') > 0):
                                    print("[Info] Replace white space in " + file_name)
                                    file_name = file_name.replace(' ', white_space_separator)

                                formatted_name = os.path.join(path, file_name)

                                #print("[Info] Rename to " + formatted_name)
                                os.rename(original_file, formatted_name)
                                i += 1