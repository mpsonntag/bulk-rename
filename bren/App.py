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
# TODO Add tests

class Main:
    @staticmethod
    def run():
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
        #main_dir_path = 'D:\\_Chaos\\DL\\handleImages\\testRename\\'
        main_dir_path = 'D:\\_Chaos\\Bilder\\201510_Zentralasien\\sorted\\'
        # Handle files in the main directory as well.
        include_main_dir = False
        # Define a base string that will be inserted into the renaming string.
        main_name = 'Zentralasien'
        # Use the name of the directory tree up to the main path when renaming a file.
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
        # TODO Current file type checks are really slow...
        rename_file_types = ['JPG', 'JPEG', 'PNG', 'GIF']
        # Define which directories within the main directory should be excluded all together.
        # This option is case sensitive.
        #exclude_dirs = ['excludeMe', '20150926_meToo']
        exclude_dirs = []

        for path, dirs, files in os.walk(main_dir_path):
            if path != main_dir_path or include_main_dir:

                # TODO add better check for exclude_dirs at this point
                exclude_dir = False
                for curr_dir in exclude_dirs:
                    if path.find(curr_dir) > -1:
                        print("[Info] Directory " + curr_dir + " will be excluded")
                        exclude_dir = True

                if not exclude_dir:
                    split_dirs = [os.path.basename(path.rstrip('\\'))]
                    if path != main_dir_path:
                        split_path = os.path.abspath(path).replace(main_dir_path, '')
                        split_dirs = split_path.split('\\')

                    print("[Info] Process directory " + path)
                    i = batch_start_index
                    for f in files:
                        original_file = os.path.join(path, f)

                        if rename_all_file_types or rename_file_types.__contains__(str(imghdr.what(original_file)).upper()):
                            if f.find(name_separator) == -1:
                                # TODO Integrate filename in a nicer way into the print string.
                                print("[Warning] File \'" + f + "\' does not contain separator")
                                # TODO Check if this is a good way to handle the file ending when
                                # TODO working with a missing name separator.
                                split_parts = f.rsplit('.', 1)
                                split_parts[1] = '.' + split_parts[1]
                            else:
                                split_parts = f.split(name_separator)

                            file_name = ""

                            # Add directory name to te current file name if set.
                            # Make sure only one white space separator is used at the
                            # end of the directory name.
                            if add_directory_name:
                                file_name += split_dirs[0].rstrip(white_space_separator)
                                file_name += white_space_separator

                            # TODO Check if inserting the main name into the first directory and any subdirectory
                            # TODO can be done in a better way.
                            file_name += main_name + white_space_separator

                            if add_directory_name:
                                for d in split_dirs[1:]:
                                    file_name += d.rstrip(white_space_separator)
                                    file_name += white_space_separator

                            file_name += "{:03d}".format(i)
                            end_name = split_parts[1]
                            if split_parts.__len__() > 2:
                                for p in split_parts[2:]:
                                    end_name += white_space_separator + p

                            file_name.strip()
                            end_name.strip()

                            if replace_white_space & (file_name.find(' ') > 0):
                                print("[Info] Replace white space in " + file_name)
                                file_name = file_name.replace(' ', white_space_separator)
                                file_name = file_name.replace(name_separator, white_space_separator)
                            if replace_white_space & (end_name.find(' ') > 0):
                                print("[Info] Replace white space in " + end_name)
                                end_name = end_name.replace(' ', white_space_separator)
                                end_name = end_name.replace(name_separator, white_space_separator)

                            file_name += name_separator + end_name

                            formatted_name = os.path.join(path, file_name)

                            os.rename(original_file, formatted_name)
                            i += 1
