# Copyright (c) 2016, Michael Sonntag (sonntag@bio.lmu.de)
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted under the terms of the BSD License. See
# LICENSE file in the root of the project.

import os

__author__ = 'Michael Sonntag'


class Main:
    def run(self):

        check_path = 'D:\\_Chaos\\Bilder\\201510 Zentralasien\\testRename\\'
        start_name = 'Zentralasien_'
        start_index = 0
        name_separator = '__'

        for path, dirs, files in os.walk(check_path):
            if path != check_path:
                i = start_index
                for f in files:
                    i += 1
                    split_parts = f.split(name_separator)
                    file_name = os.path.basename(path) + start_name + "{:03d}".format(i)
                    file_name += name_separator + split_parts[1]
                    formatted_name = os.path.join(path, file_name)

                    os.rename(os.path.join(path, f), formatted_name)

Main().run()