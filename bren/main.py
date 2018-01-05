# Copyright (c) 2017, Michael Sonntag (sonntag@bio.lmu.de)
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted under the terms of the BSD License. See
# LICENSE file in the root of the project.

from .BulkRename import BulkRename

# tmp arguments until we add command line parser
work_dir = "/nothing/to/see/here/"
base_name = "hurra"
config_file = "/tmp/some/file.yml"


def run():
    BulkRename(work_dir).run()


if __name__ == '__main__':
    print("main")
