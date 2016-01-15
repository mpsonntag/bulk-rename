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


class Main:
    def run(self):
        """Script used to batch rename files in a directory tree. At the moment only files in the
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
        main_name = 'Zentralasien_'
        # Define at which number the index for renaming multiple files in each folder should start.
        batch_start_index = 1
        # Separator string that separates the part of the existing filename that will be
        # replaced with the part of the existing filename that will be kept for the renaming string.
        name_separator = '__'
        # Define if all files encountered in a directory should be renamed
        # or if only a defined subset should be subjected to renaming.
        rename_all_file_types = False
        # Define which types of files should be renamed.
        rename_file_types = ['JPG', 'JPEG', 'PNG']
        # Define which directories within the main directory should be excluded all together.
        exclude_dirs = ['excludeMe']

        for path, dirs, files in os.walk(main_dir_path):
            if path != main_dir_path:

                # TODO add check for exclude_dirs at this point

                i = batch_start_index
                for f in files:
                    original_file = os.path.join(path, f)

                    if rename_all_file_types or rename_file_types.__contains__(str(imghdr.what(original_file)).upper()):
                        if not f.__contains__(name_separator):
                            # TODO integrate filename in a nicer way into the print string
                            print("[Warning] File \'"+ f +"\' does not contain separator")
                            break

                        split_parts = f.split(name_separator)
                        file_name = os.path.basename(path) + main_name + "{:03d}".format(i)
                        file_name += name_separator + split_parts[1]
                        formatted_name = os.path.join(path, file_name)
                        #print(formatted_name)
                        #os.rename(original_file, formatted_name)
                        i += 1

Main().run()