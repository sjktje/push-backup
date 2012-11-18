#!/usr/bin/env python
# -*- coding: utf8 -*-

# Copyright (c) 2012 Svante Kvarnström <sjk@ankeborg.nu>. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import argparse
import sys

from config import Config
from rsync import Rsync, Utils

def run(argv):
    parser = argparse.ArgumentParser(
            description='Add a more elaborate description here, later.'
    )

    parser.add_argument('-v', '--verbose', action='store_true',
                        help='throw a racket about what we are doing')
    parser.add_argument('-V', '--version', action='version',
                        version='%(prog)s 0.1-alpha')
    args = parser.parse_args(argv)

    conf = Config()

    if args.verbose:
        conf.verbose = True

    utils = Utils()

    if not utils.exists_rsync():
        print "Could not find rsync -- is it installed?"
        sys.exit(1)

    if not utils.check_version((3,0,9)):
        print "Installed rsync is too old. Please upgrade!"
        sys.exit(1)


    for server in conf.servers:
        rsync = Rsync(server, conf)
        rsync.run()
