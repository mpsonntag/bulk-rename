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

        check_path = 'D:\\_Chaos\\Bilder\\201510_Zentralasien\\testRename\\'
        main_name = 'Zentralasien_'
        batch_start_index = 1
        name_separator = '__'
        rename_type = ['JPG', 'JPEG', 'PNG']
        rename_all = True

        for path, dirs, files in os.walk(check_path):
            if path != check_path:
                i = batch_start_index
                for f in files:
                    original_file = os.path.join(path, f)

                    if rename_all or rename_type.__contains__(str(imghdr.what(original_file)).upper()):
                        if not f.__contains__(name_separator):
                            print("[Warning] File %s does not contain separator", f)
                            break

                        split_parts = f.split(name_separator)
                        file_name = os.path.basename(path) + main_name + "{:03d}".format(i)
                        file_name += name_separator + split_parts[1]
                        formatted_name = os.path.join(path, file_name)
                        print(formatted_name)
                        os.rename(original_file, formatted_name)
                        i += 1

Main().run()