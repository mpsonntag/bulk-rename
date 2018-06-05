"""
Copyright (c) 2017, Michael Sonntag (sonntag@bio.lmu.de)

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted under the terms of the BSD License. See
LICENSE file in the root of the project.
"""

import os
import imghdr
import yaml

# TODO Add start and end
# TODO Add logfile
# TODO Add commandline support - add cmdline parser


class BulkRename:

    def __init__(self, main_dir_path, base_name="baseName", config_file=None):

        # Set defaults
        self.include_main_dir = False
        self.add_directory_name = True
        self.name_separator = "__"
        self.replace_white_space = True
        self.white_space_separator = "_"
        self.batch_start_index = 1
        self.rename_everything = True
        # TODO Current file type checks are really slow...
        self.rename_file_types = ['JPG', 'JPEG', 'PNG', 'GIF']
        self.exclude_dirs = []

        # Set semi-configs
        self.main_dir_path = main_dir_path
        self.base_name = base_name

        # Set config if available
        print("[Info] Using config file: %s (found: %s)" %
              (config_file, os.path.isfile(config_file)))

        if config_file and os.path.isfile(config_file):
            with open(config_file) as yaml_raw:
                cfg = yaml.load(yaml_raw)
                if "include_main_dir" in cfg and cfg["include_main_dir"]:
                    self.include_main_dir = self._bool_switch(cfg["include_main_dir"])
                if "add_directory_name" in cfg and cfg["add_directory_name"]:
                    self.add_directory_name = self._bool_switch(cfg["add_directory_name"])
                if "name_separator" in cfg and cfg["name_separator"]:
                    self.name_separator = cfg["name_separator"]
                if "replace_white_space" in cfg and cfg["replace_white_space"]:
                    self.replace_white_space = cfg["replace_white_space"]
                if "white_space_separator" in cfg and cfg["white_space_separator"]:
                    self.white_space_separator = cfg["white_space_separator"]
                if "batch_start_index" in cfg and cfg["batch_start_index"]:
                    try:
                        2 + cfg["batch_start_index"]
                    except TypeError as _:
                        print("[Warning] Invalid start index '%s'; using 1" %
                              cfg["batch_start_index"])
                    else:
                        self.batch_start_index = cfg["batch_start_index"]
                if "rename_everything" in cfg and cfg["rename_everything"]:
                    self.rename_everything = self._bool_switch(cfg["rename_everything"])
                if "rename_file_types" in cfg and cfg["rename_file_types"]:
                    self.rename_file_types = cfg["rename_file_types"]
                if "exclude_dirs" in cfg and cfg["exclude_dirs"]:
                    self.exclude_dirs = cfg["exclude_dirs"]

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
              (self.base_name, self.add_directory_name, self.batch_start_index))
        print("[Info] Separator: '%s'; ws separator: '%s'; replace ws: '%s'" %
              (self.name_separator, self.white_space_separator, self.replace_white_space))
        print("[Info] Rename file types: %s" % self.rename_file_types)

        for path, _, files in os.walk(self.main_dir_path):
            if path != self.main_dir_path or self.include_main_dir:

                # TODO Add better check for exclude_dirs at this point
                exclude_dir = False
                for curr_dir in self.exclude_dirs:
                    if path.find(curr_dir) > -1:
                        print("[Info] Directory '%s' will be excluded" % curr_dir)
                        exclude_dir = True

                if not exclude_dir:
                    split_dirs = [os.path.basename(path.rstrip("\\"))]
                    if path != self.main_dir_path:
                        split_path = os.path.abspath(path).replace(self.main_dir_path, "")
                        split_dirs = split_path.split("\\")

                    print("[Info] Processing directory '%s'" % path)
                    i = self.batch_start_index
                    for curr in files:
                        self._rename(path, curr, split_dirs, i)
                        i += 1

    def _rename(self, path, curr_file, split_dirs, idx):
        original_file = os.path.join(path, curr_file)

        fpc = str(imghdr.what(original_file)).upper()
        if self.rename_everything or (fpc in self.rename_file_types):
            if curr_file.find(self.name_separator) == -1:
                print("[Warning] File '%s' does not contain separator" % curr_file)

                # TODO Check if this is a good way to handle the file extension
                # when working with a missing name separator.

                split_parts = curr_file.rsplit(".", 1)
                split_parts[1] = ".%s" % split_parts[1]
            else:
                split_parts = curr_file.split(self.name_separator)

            file_name = ""

            # Add directory name to the current file name if set.
            # Make sure only one white space separator is used at the
            # end of the directory name.
            if self.add_directory_name:
                file_name += split_dirs[0].rstrip(self.white_space_separator)
                file_name += self.white_space_separator

            # TODO Check if inserting the main name into the first
            # directory and any subdirectory can be done in a better way.
            file_name += self.base_name + str(self.white_space_separator)

            if self.add_directory_name:
                for curr_dir in split_dirs[1:]:
                    file_name += curr_dir.rstrip(self.white_space_separator)
                    file_name += self.white_space_separator

            file_name += "{:03d}".format(idx)
            end_name = split_parts[1]
            if split_parts.__len__() > 2:
                for part in split_parts[2:]:
                    end_name += self.white_space_separator + part

            file_name.strip()
            end_name.strip()

            if self.replace_white_space & (file_name.find(" ") > 0):
                print("[Info] Replace white space in %s" % file_name)
                file_name = file_name.replace(" ", self.white_space_separator)
                file_name = file_name.replace(self.name_separator,
                                              self.white_space_separator)
            if self.replace_white_space & (end_name.find(" ") > 0):
                print("[Info] Replace white space in %s" % end_name)
                end_name = end_name.replace(" ", self.white_space_separator)
                end_name = end_name.replace(self.name_separator,
                                            self.white_space_separator)

            file_name += self.name_separator + end_name

            formatted_name = os.path.join(path, file_name)

            os.rename(original_file, formatted_name)

    @staticmethod
    def _bool_switch(value):
        if value == 1:
            return True
        return False
