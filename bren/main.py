# Copyright (c) 2017, Michael Sonntag (sonntag@bio.lmu.de)
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted under the terms of the BSD License. See
# LICENSE file in the root of the project.

from .BulkRename import BulkRename


def run():
    BulkRename.run()


if __name__ == '__main__':
    print("main")
